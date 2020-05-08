BIN_DIR = ./bin
INC_DIR = ./include
OBJ_DIR = ./obj
SRC_DIR = ./src

# DIRS = $(BIN_DIR) $(INC_DIR) $(SRC_DIR)

DEPS = token.h interpreter.h
SRC_FILES = main.cpp interpreter.cpp token.cpp

EXECUTABLE_NAME = main

CC = g++

# MODIFY ABOVE ONLY =========================

# Selective search variables
vpath %.h $(INC_DIR)
vpath %.o $(BIN_DIR)
vpath %.cpp $(SRC_DIR)

# Compilation variables
CFLAGS = -I$(INC_DIR)
OUTPUT_OPTION = -o $(OBJ_DIR)/$@

# File generation
EXECUTABLE = $(EXECUTABLE_NAME:%=$(BIN_DIR)/%)
OBJ_FILES = $(SRC_FILES:%.cpp=$(OBJ_DIR)/%.o)

$(EXECUTABLE): $(OBJ_FILES)
	$(CC) -o $@ $(OBJ_FILES)

$(OBJ_DIR)/%.o: %.cpp $(DEPS) | $(OBJ_DIR)
	$(CC) -c $< -o $@ $(CFLAGS)
 
$(OBJ_DIR):
	mkdir $(OBJ_DIR)

.PHONY: build clean
build: $(EXECUTABLE)
	$(EXECUTABLE)
clean:
	rm $(OBJ_DIR) -r $(EXECUTABLE)