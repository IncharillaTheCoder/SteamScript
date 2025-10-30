import re
import sys
import os

class SteamScriptInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        
    def interpret(self, code):
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            self.execute_line(line)
    
    def execute_line(self, line):
        if line.startswith('warm '):
            match = re.match(r'warm (.+?) = (.+)', line)
            if match:
                var_name = match.group(1).strip()
                value = self.evaluate_expression(match.group(2).strip())
                self.variables[var_name] = value
                return

        if line.startswith('kettle '):
            match = re.match(r'kettle (.+?)\((.*?)\) \{ (.+) \}', line)
            if match:
                func_name = match.group(1).strip()
                params = [p.strip() for p in match.group(2).split(',')] if match.group(2) else []
                body = match.group(3).strip()
                self.functions[func_name] = {'params': params, 'body': body}
                return

        if '(' in line and ')' in line and not line.startswith('if'):
            match = re.match(r'(.+?)\((.*?)\)', line)
            if match:
                func_name = match.group(1).strip()
                args = [self.evaluate_expression(arg.strip()) for arg in match.group(2).split(',')] if match.group(2) else []
                self.call_function(func_name, args)
                return

        if line.startswith('if '):
            self.execute_if(line)
            return

        if any(line.startswith(keyword) for keyword in ['sip ', 'enjoy ', 'drink ']):
            for keyword in ['sip ', 'enjoy ', 'drink ']:
                if line.startswith(keyword):
                    expr = line[len(keyword):].strip()
                    value = self.evaluate_expression(expr)
                    print(f"☕ {value}")
                    return
    
    def evaluate_expression(self, expr):
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        if expr.isdigit():
            return int(expr)

        if expr in self.variables:
            return self.variables[expr]

        if '+' in expr:
            parts = expr.split('+')
            return str(self.evaluate_expression(parts[0])) + str(self.evaluate_expression(parts[1]))
          
        if '*' in expr:
            parts = expr.split('*')
            return self.evaluate_expression(parts[0]) * self.evaluate_expression(parts[1])
        
        return expr
    
    def call_function(self, func_name, args):
        if func_name in self.functions:
            func = self.functions[func_name]
            original_vars = self.variables.copy()
            for param, arg in zip(func['params'], args):
                self.variables[param] = arg

            body = func['body']
            if body.startswith('pour '):
                result = self.evaluate_expression(body[5:])
                print(f"🫖 {result}")

            self.variables = original_vars
    
    def execute_if(self, line):
        if '{' in line and '}' in line:
            then_part = line.split('{')[1].split('}')[0].strip()
            self.execute_line(then_part)

def run_file(filename):
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        print("💡 Maybe your tea went cold? Try a different filename.")
        return
    
    print(f"🚂 STEAMSCRIPT: Brewing {filename}...")
    print("=" * 50)
    
    with open(filename, 'r') as file:
        code = file.read()
    
    interpreter = SteamScriptInterpreter()
    interpreter.interpret(code)
    
    print("=" * 50)
    print("🏁 PROGRAM FINISHED - Time for a cozy break! 🫖")

def main():
    if len(sys.argv) != 2:
        print("🎯 SteamScript Interpreter")
        print("Usage: python steamscript.py <filename.tea>")
        print("\nExample:")
        print("  python steamscript.py hello_world.tea")
        print("\nOr make it executable:")
        print("  chmod +x steamscript.py")
        print("  ./steamscript.py hello_world.tea")
        return
    
    filename = sys.argv[1]
    run_file(filename)

if __name__ == "__main__":
    main()
