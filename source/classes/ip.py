"""
File dedicated to the IPAdress class
"""


class IPAddress:
    """
    Defines an ip adress, has methods to test and separate it into it's constituent octets
    """

    def __init__(self, address: str):
        self.address = address

    def __str__(self):
        return self.address

    def is_valid(self):
        """
        Checks if it's a valid IP address.

        Returns:
            bool: True if the IP address is valid, False otherwise.
        """
        try:
            # Split the address into octets and ensure there are exactly 4 octets
            octets = list(map(int, self.address.split(".")))
            if len(octets) != 4:
                return False

            # Check if each octet is within the valid range [0, 255]
            if not all(0 <= octet <= 255 for octet in octets):
                return False

            return True

        except ValueError:
            # ValueError may occur if an octet is not a valid integer
            return False

    def get_octets(self):
        """
        Return the octets as a list of integers

        Might return none, remember to validade the ip!
        """
        try:
            octets = list(map(int, self.address.split(".")))
            return octets
        except ValueError:
            return None
