CC = g++

BIN_DIR = ./bin
INC_DIR = ./inc
OBJ_DIR = ./obj
SRC_DIR = ./src

vpath %.cpp $(SRC_DIR) 
vpath %.h $(INC_DIR)
vpath %.o $(OBJ_DIR)

SRC_FILES = ast_visitor.cpp interpreter.cpp lexer.cpp parser.cpp token.cpp main.cpp
OBJ_FILES = $(SRC_FILES:%.cpp=%.o)

EXECUTABLE_NAME = main
EXECUTABLE = $(BIN_DIR)/$(EXECUTABLE_NAME)

CFLAGS = -I$(INC_DIR)

#=================================================

$(EXECUTABLE): $(OBJ_FILES)
	$(CC) -o $(EXECUTABLE) $(addprefix $(OBJ_DIR)/,$(OBJ_FILES))

main.o: main.cpp interpreter.h lexer.h parser.h ast_visitor.h utils.h | $(OBJ_DIR)
	$(CC) -c $(SRC_DIR)/main.cpp -o $(OBJ_DIR)/main.o $(CFLAGS)

ast_visitor.o: ast_visitor.cpp token.h | $(OBJ_DIR)
	$(CC) -c $(SRC_DIR)/ast_visitor.cpp -o $(OBJ_DIR)/$@ $(CFLAGS)

interpreter.o: interpreter.cpp ast_visitor.h parser.h token.h | $(OBJ_DIR)
	$(CC) -c $(SRC_DIR)/interpreter.cpp -o $(OBJ_DIR)/$@ $(CFLAGS)	

lexer.o: lexer.cpp token.h utils.h | $(OBJ_DIR)
	$(CC) -c $(SRC_DIR)/lexer.cpp -o $(OBJ_DIR)/$@ $(CFLAGS)	

parser.o: parser.cpp ast_visitor.h lexer.h token.h | $(OBJ_DIR)
	$(CC) -c $(SRC_DIR)/parser.cpp -o $(OBJ_DIR)/$@ $(CFLAGS)	

token.o: token.cpp | $(OBJ_DIR)
	$(CC) -c $(SRC_DIR)/token.cpp -o $(OBJ_DIR)/$@ $(CFLAGS)	

utils.o: utils.cpp | $(OBJ_DIR)
	$(CC) -c $(SRC_DIR)/utils.cpp -o $(OBJ_DIR)/$@ $(CFLAGS)

$(OBJ_DIR):
	mkdir $(OBJ_DIR)

#=================================================

.PHONY: build clean

build: $(EXECUTABLE) 
	$(EXECUTABLE) 

clean:
	rm $(EXECUTABLE) $(OBJ_DIR) -r