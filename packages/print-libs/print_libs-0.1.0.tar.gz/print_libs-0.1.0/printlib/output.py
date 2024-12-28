class ColoredOutput:
    COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }
    
    def __init__(self):
        pass
    
    def print_colored(self, text, color="white"):
        """输出带颜色的文本，支持多种数据类型"""
        if color not in self.COLORS:
            print("Invalid color! Using default color.")
            color = "white"
        if isinstance(text, (list, tuple)):
            text = "\n".join([str(item) for item in text])
        elif isinstance(text, dict):
            text = "\n".join([f"{key}: {value}" for key, value in text.items()])
        elif not isinstance(text, str):
            text = repr(text)
        
        # 颜色格式化
        color_code = self.COLORS[color]
        reset_code = self.COLORS["reset"]
        print(f"{color_code}{text}{reset_code}")
    
    def red(self, text):
        """输出红色文本"""
        self.print_colored(text, "red")
    
    def green(self, text):
        """输出绿色文本"""
        self.print_colored(text, "green")
    
    def yellow(self, text):
        """输出黄色文本"""
        self.print_colored(text, "yellow")
    
    def blue(self, text):
        """输出蓝色文本"""
        self.print_colored(text, "blue")
    
    def magenta(self, text):
        """输出品红色文本"""
        self.print_colored(text, "magenta")
    
    def cyan(self, text):
        """输出青色文本"""
        self.print_colored(text, "cyan")
        
OUTPUT = ColoredOutput()
