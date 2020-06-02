from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from visitor import SemanticAnalyzer, SourceToSourceCompiler

###############################################################################
#                                                                             #
#  MAIN                                                                       #
#                                                                             #
###############################################################################

if __name__ == "__main__":
   code = """
program Main;
   var b, x, y : real;
   z : integer;

   procedure AlphaA(a,a : integer);
      var b : integer;

      procedure Beta(c : integer);
         var y : integer;

         procedure Gamma(c : integer);
            var x : integer;
         begin { Gamma }
            x := a + b + c + x + y + z;
         end;  { Gamma }

      begin { Beta }

      end;  { Beta }

   begin { AlphaA }

   end;  { AlphaA }

   procedure AlphaB(a : integer);
      var c : real;
   begin { AlphaB }
      c := a + b;
   end;  { AlphaB }

begin { Main }
end.  { Main }
    """
    #print(f"Input: {code}")

   lexer = Lexer(code)
   parser = Parser(lexer)
   tree_head = parser.parse()

   sem_analyzer = SemanticAnalyzer()
   sem_analyzer.visit_ProgramNode(tree_head)

   #  comp = SourceToSourceCompiler()
   #  comp.visit(tree_head)
   #  print(comp.code)

   interpreter = Interpreter(tree_head)
   interpreter.interpret()
   print("Result:", interpreter.global_memory)
