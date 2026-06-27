from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from django.conf import settings
import os
import requests as http_requests

from .serializers import RegisterSerializer
from .models import OTPVerification, UserProfile
from .email_service import send_otp_email
from chat.models import UserPersonality


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"].strip().lower()

        if User.objects.filter(email=email).exists():
            return Response({"error": "An account with this email already exists."}, status=400)

        # Create user as inactive until email is verified
        user = serializer.save()
        user.is_active = False
        user.save(update_fields=["is_active"])

        # Create profile
        UserProfile.objects.get_or_create(user=user)

        # Generate and send OTP
        otp = OTPVerification.generate_for_user(user)
        send_otp_email(email, email, otp.code)

        return Response({
            "message": "Account created. Please check your email for your verification code.",
            "email": email
        }, status=201)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        code = request.data.get("code", "").strip()

        if not email or not code:
            return Response({"error": "Email and code are required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No account found with this email."}, status=404)

        otp = OTPVerification.objects.filter(
            user=user,
            code=code,
            is_used=False
        ).order_by("-created_at").first()

        if not otp or not otp.is_valid():
            return Response({"error": "Invalid or expired code. Please request a new one."}, status=400)

        # Mark OTP used
        otp.is_used = True
        otp.save(update_fields=["is_used"])

        # Activate user
        user.is_active = True
        user.save(update_fields=["is_active"])

        # Mark profile verified
        UserProfile.objects.filter(user=user).update(is_email_verified=True)

        # Return tokens — logged in immediately after verification
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "Email verified successfully.",
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "email": user.email,
        })


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()

        if not email:
            return Response({"error": "Email is required."}, status=400)

        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            return Response({"error": "No unverified account found with this email."}, status=404)

        otp = OTPVerification.generate_for_user(user)
        send_otp_email(email, email, otp.code)

        return Response({"message": "A new verification code has been sent to your email."})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password", "")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=401)

        # Check if email is verified
        if not user.is_active:
            return Response({
                "error": "Please verify your email before logging in.",
                "requires_verification": True,
                "email": email
            }, status=403)

        # authenticate uses username internally — since you set username=email in serializer this works
        authenticated_user = authenticate(username=email, password=password)
        if not authenticated_user:
            return Response({"error": "Invalid email or password."}, status=401)

        tokens = get_tokens_for_user(authenticated_user)
        return Response({
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "email": authenticated_user.email,
        })


class GoogleAuthInitView(APIView):
    """
    Step 1 — Frontend hits this to get the Google login URL.
    It redirects the user to Google's consent screen.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account",
        }
        from urllib.parse import urlencode
        url = f"{google_auth_url}?{urlencode(params)}"
        return Response({"url": url})


class GoogleAuthCallbackView(APIView):
    """
    Step 2 — Google redirects back here with a code.
    We exchange it for user info, create or fetch the user, and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "No authorization code provided."}, status=400)

        # Exchange code for access token
        token_response = http_requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )

        token_data = token_response.json()

        if "error" in token_data:
            return Response({"error": token_data.get("error_description", "Google auth failed.")}, status=400)

        access_token = token_data.get("access_token")

        # Use access token to get user info from Google
        user_info_response = http_requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        user_info = user_info_response.json()

        email = user_info.get("email", "").lower()
        name = user_info.get("name", "")
        google_id = user_info.get("id", "")
        is_verified = user_info.get("verified_email", False)

        if not email:
            return Response({"error": "Could not retrieve email from Google."}, status=400)

        if not is_verified:
            return Response({"error": "Your Google email is not verified."}, status=400)

        # Get or create the user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "first_name": name.split()[0] if name else "",
                "last_name": " ".join(name.split()[1:]) if len(name.split()) > 1 else "",
                "is_active": True,
            }
        )

        if created:
            # Set unusable password since they log in via Google
            user.set_unusable_password()
            user.save()

            # Create profile and personality for new users
            UserProfile.objects.get_or_create(user=user, defaults={"is_email_verified": True})
            UserPersonality.objects.get_or_create(user=user)

        else:
            # Existing user — make sure they're active and verified
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
            UserProfile.objects.filter(user=user).update(is_email_verified=True)

        tokens = get_tokens_for_user(user)
        return Response({
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "email": user.email,
            "name": name,
            "is_new_user": created,
        })