from pyfingerprint.pyfingerprint import PyFingerprint

try:
    # Initialize sensor on your FTDI COM port
    f = PyFingerprint('COM6', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('Failed to initialize sensor:')
    print(e)
    exit(1)

print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

## Enroll new fingerprint
try:
    print('Waiting for finger...')

    # Wait until finger is read
    while not f.readImage():
        pass

    # Convert image
    f.convertImage(0x01)

    # Search the finger to avoid duplicates
    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        print('Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    while f.readImage():
        pass

    print('Place the same finger again...')
    while not f.readImage():
        pass

    # Convert image again
    f.convertImage(0x02)

    # Create template
    if f.createTemplate():
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('Stored at position #' + str(positionNumber))

except Exception as e:
    print('Operation failed!')
    print(e)
    exit(1)
