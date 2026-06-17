import random

# Generate a 6-digit OTP
def generate_otp():
    otp = random.randint(100000, 999999)
    return str(otp)

# Verify OTP
def verify_otp(user_otp, actual_otp):
    return user_otp == actual_otp


# Example
if __name__ == "__main__":
    otp = generate_otp()
    print("Generated OTP:", otp)

    user_input = input("Enter OTP: ")

    if verify_otp(user_input, otp):
        print("OTP Verified Successfully!")
    else:
        print("Invalid OTP!")