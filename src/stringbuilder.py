class StringBuilder:
    def __init__(self):
        self.string = ""
    def stringForTime(hours: float)-> str:
        total_hours = hours
        # Convert hours to days
        days = int(hours / 24)
        # Calculate the number of years by dividing the number of days by 365
        years = int(days / 365)
        # Calculate the number of months by dividing the remaining number of days by 30 (approximate)
        months = int((days % 365) / 30)
        # Calculate the number of remaining days
        days = int((days % 365) % 30)
        # Calculate the number of remaining hours
        hours = int(hours % 24)

        # Create the string representation of the time
        time_string = ""
        if years > 0:
            time_string += f"{years} Jahr" + "e" if years > 1 else ""
            if months > 0:
                time_string += f",{months} Monat" + "e" if months > 1 else ""
            if days > 0:
                time_string += f",{days} Tag" + "e" if days > 1 else ""
            if hours > 0:
                time_string += f",{hours} Stunde" + "n" if hours > 1 else ""
        elif months > 0:
            time_string += f"{months} Monat" + "e" if months > 1 else ""
            if days > 0:
                time_string += f",{days} Tag" + "e" if days > 1 else ""
            if hours > 0:
                time_string += f",{hours} Stunde" + "n" if hours > 1 else ""
        elif days > 0:
            time_string += f"{days} Tag" + "e" if days > 1 else ""
            if hours > 0:
                time_string += f"{hours} Stunde" + "n" if hours > 1 else ""
        elif hours > 0:
            time_string += f"{hours} Stunde" + "n" if hours > 1 else ""

        return time_string+" ("+str(total_hours)+"h)"




            
        
        