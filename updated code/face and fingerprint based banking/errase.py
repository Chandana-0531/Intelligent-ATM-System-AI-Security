from pyfingerprint.pyfingerprint import PyFingerprint

try:
    # Adjust COM port and baud as per your setup
    f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError("Fingerprint sensor password is wrong!")

except Exception as e:
    print("❌ Failed to initialize fingerprint sensor:", e)
    exit(1)

print("⚠️ Deleting all fingerprints...")

try:
    f.clearDatabase()
    print("✅ All fingerprints deleted successfully!")

except Exception as e:
    print("❌ Failed to delete fingerprints:", e)
