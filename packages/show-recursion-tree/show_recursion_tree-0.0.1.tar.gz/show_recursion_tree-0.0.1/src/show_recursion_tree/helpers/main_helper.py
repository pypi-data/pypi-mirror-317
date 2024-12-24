

def normalize_args_kwargs(args, kwargs) -> str:
    """
    turn args + kwargs into human-readable string
        - ()
    """
    content: str = ""
    if args:
        content += str(args)[1:-1]  # remove brackets
    if kwargs:
        content += ", ".join([f"{k}={v}" for k,v in kwargs.items()])
    
    return f"({content})"