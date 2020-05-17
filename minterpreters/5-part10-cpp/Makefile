CC = g++

BIN_DIR = ./bin
INC_DIR = ./inc
OBJ_DIR = ./obj
SRC_DIR = ./src

vpath %.cpp $(SRC_DIR) 
vpath %.h $(INC_DIR)

MAIN_NAME = main
SRC_FILES = interpreter.cpp lexer.cpp parser.cpp token.cpp ast_visitor.cpp
OBJ_FILES = $(SRC_FILES:%.cpp=$(OBJ_DIR)/%.o)

EXECUTABLE_NAME = main
EXECUTABLE = $(BIN_DIR)/$(EXECUTABLE_NAME)

CFLAGS = -I$(INC_DIR)

#=================================================

$(EXECUTABLE): $(OBJ_FILES) $(OBJ_DIR)/$(MAIN_NAME).o
	$(CC) $^ -o $(EXECUTABLE) 

# The [main].cpp file won't have an associated .h file so is done separately.
$(OBJ_DIR)/$(MAIN_NAME).o: $(SRC_DIR)/$(MAIN_NAME).cpp $(INC_DIR)/lexer.h | $(OBJ_DIR)
	$(CC) -c $< -o $@ -I./inc

# Lexer depends on token
$(OBJ_DIR)/lexer.o: $(SRC_DIR)/lexer.cpp $(INC_DIR)/lexer.h $(SRC_DIR)/token.cpp | $(OBJ_DIR)
	$(CC) -c $< -o $@ -I./inc

# All remaining object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp $(INC_DIR)/%.h | $(OBJ_DIR)
	$(CC) -c $< -o $@ $(CFLAGS)

$(OBJ_DIR):
	mkdir $(OBJ_DIR)

#=================================================

.PHONY: build clean

build: $(EXECUTABLE) 
	$(EXECUTABLE) 

clean:
	rm $(EXECUTABLE) $(OBJ_DIR) -r