from pyfingerprint.pyfingerprint import PyFingerprint

try:
    f = PyFingerprint('/dev/fp_in', 57600)

    if f.verifyPassword() == False:
        raise ValueError('Sensor password incorrect')

    print('Waiting for finger...')

    while f.readImage() == False:
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()

    positionNumber = result[0]

    if positionNumber == -1:
        print('No match found')
    else:
        print('Match found at position:', positionNumber)

except Exception as e:
    print('Operation failed!')
    print(e)