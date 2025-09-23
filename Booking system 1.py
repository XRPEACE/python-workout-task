class Booking:
    _booking_counter = 1
    all_bookings = {}

    def __init__(self, customer_name, booking_type, details):
        if booking_type not in ("flight", "hotel"):
            raise ValueError("booking_type must be 'flight' or 'hotel'")
        self.customer_name = customer_name
        self.booking_type = booking_type
        self.details = details
        self.status = "pending"
        self.booking_id = f"B{Booking._booking_counter}"
        Booking._booking_counter += 1

    def __str__(self):
        if self.booking_type == "flight":
            dest = self.details.get("destination", "")
            return f"Booking [{self.booking_id}]: {self.customer_name} - {self.status.title()} Flight to {dest}"
        elif self.booking_type == "hotel":
            hotel = self.details.get("hotel_name", "")
            return f"Booking [{self.booking_id}]: {self.customer_name} - {self.status.title()} Hotel at {hotel}"
        return f"Booking [{self.booking_id}]: {self.customer_name} - {self.status.title()}"

    def __repr__(self):
        return f"Booking('{self.customer_name}', '{self.booking_type}', {self.details})"

    def confirm(self):
        if self.status == "pending":
            self.status = "confirmed"
            print(f"Booking {self.booking_id} confirmed.")
        elif self.status == "confirmed":
            print(f"Booking {self.booking_id} is already confirmed.")
        else:
            print(
                f"Booking {self.booking_id} cannot be confirmed because it is {self.status}.")

    def cancel(self):
        if self.status != "cancelled":
            self.status = "cancelled"
            print(f"Booking {self.booking_id} cancelled.")
        else:
            print(f"Booking {self.booking_id} is already cancelled.")

    @classmethod
    def create_booking(cls, customer_name, booking_type, details):
        booking = cls(customer_name, booking_type, details)
        cls.all_bookings[booking.booking_id] = booking
        return booking

    @classmethod
    def find_booking(cls, booking_id):
        return cls.all_bookings.get(booking_id)

    @classmethod
    def list_all(cls):
        for booking in cls.all_bookings.values():
            print(booking)


# --- Test section ---
if __name__ == "__main__":
    b1 = Booking.create_booking("John Doe", "flight", {
        "origin": "JFK", "destination": "LAX", "flight_number": "UA123"
    })

    b2 = Booking.create_booking("Jane Smith", "hotel", {
        "hotel_name": "Grand Hyatt", "room_type": "Suite", "nights": 3
    })

    print(b1)
    print(b2)
    b1.confirm()
    b2.cancel()
    print(b1)
    print(b2)
