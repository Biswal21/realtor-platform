from rest_framework.throttling import AnonRateThrottle


class VerifyOTPThrottle(AnonRateThrottle):
    scope = "verify_otp"


class OTPGenerationThrottle(AnonRateThrottle):
    scope = "otp_generation"
