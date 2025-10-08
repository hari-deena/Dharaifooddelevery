
# Generates a confirmation message with booking date, time, and amount paid.
def generate_booking_confirmation(formatted_date, formatted_start_time, formatted_end_time, total_amount):
    confirmation_message = (
        "Thank you for confirming your booking! Here are your reservation details:\n"
        f"- Date: {formatted_date}\n"
        f"- Time: {formatted_start_time} to {formatted_end_time}\n"
        f"- Amount Paid: ₹{total_amount}"
    )
    return confirmation_message

# Generates a cancellation message with booking date, time, and canceled amount
def generate_booking_cancellation(formatted_date, formatted_start_time, formatted_end_time, cancel_amount):
    cancellation_message = (
        "Your booking has been successfully cancelled. Here are the details of your cancelled reservation:\n"
        f"- Date: {formatted_date}\n"
        f"- Time: {formatted_start_time} to {formatted_end_time}\n"
        f"- Cancelled Amount: ₹{cancel_amount}"
    )
    return cancellation_message

# Generates a completed booking message with full booking details and a thank-you note.
def generate_booking_completed(formatted_date, formatted_start_time, formatted_end_time, total_amount):
    confirmation_message = (
        " Booking Completed Successfully! \n"
        "Thank you for your booking. Here are your reservation details:\n"
        f"- Date: {formatted_date}\n"
        f"- Time: {formatted_start_time} to {formatted_end_time}\n"
        f"- Amount Paid: ₹{total_amount}\n"
        "We look forward to seeing you. Enjoy your game!"
    )
    return confirmation_message

# Generates a message explaining turf cancellation due to inactivity, along with refund details and an apology.
def generate_turf_inactive_cancellation(formatted_date, formatted_start_time, formatted_end_time, refund_amount):
    cancellation_message = (
        "We regret to inform you that your booking has been cancelled due to the turf being temporarily inactive by the turf management.\n\n"
        "Here are the details of your cancelled reservation:\n"
        f"- Date: {formatted_date}\n"
        f"- Time: {formatted_start_time} to {formatted_end_time}\n"
        f"- Refunded Amount: ₹{refund_amount}\n\n"
        "We apologize for the inconvenience caused. The refunded amount will be credited to your original payment method shortly. "
        "Thank you for your understanding."
    )
    return cancellation_message

def generate_turf_booking_confirmation_nad_cancelation(turf_name, start_time, end_time):
    return f"{turf_name} at \"{start_time} - {end_time}\""
