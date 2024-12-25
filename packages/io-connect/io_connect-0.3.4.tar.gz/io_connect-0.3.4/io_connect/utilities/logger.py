import sys



def display_log(log: str):
    """
    Display a log message on the console.

    This function writes a log message to the standard output stream (stdout), 
    overwriting any existing content on the current line.

    Args:
        log (str): The log message to be displayed.

    Returns:
        None

     Example:
        >>> display_log("Processing...")  # Displays "Processing..." on the console
    
    """

    # Move the cursor to the beginning of the line
    sys.stdout.write('\r')
    
    # Write the log message
    sys.stdout.write(log)
    
    # Flush the output buffer to ensure the message is displayed immediately
    sys.stdout.flush()