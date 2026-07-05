def hex_to_characteristics(hex_string):

    return [

        int(hex_string[i:i+2], 16)

        for i in range(

            0,

            len(hex_string),

            2

        )

    ]