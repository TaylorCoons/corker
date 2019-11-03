#!/usr/bin/python3

import os
import re
import copy


class Keyword:
    
    name = None
    keyword = None
    
    def __init__(self, name, keyword):
        self.name = name
        self.keyword = keyword

    def __repr__(self):
        return 'Keyword()'
    
    def __str__(self):
        return '{}\t{}'.format(self.name, self.keyword)


class ObjectType:
    
    objType = None
    objName = None
    state = None
    
    def __init__(self, objType, objName, state):
        self.objType = objType
        self.objName = objName
        self.state = state

 
    def __repr__(self):
        return 'ObjectType()'

    
    def __str__(self):
        return '<{}, {}, {}>'.format(
            self.objType, 
            self.objName,
            self.state
        )

    
    def __eq__(self, other):
        if (
            self.objType == other.objType
            and self.objName == other.objName
            and self.state == other.state
           ):
            return True
        return False


class State:
    
    visibility = None
    scope = None
    
    def __init__(self, visibility, scope):
        self.visibility = visibility
        self.scope = scope


    def __repr__(self):
        return 'State()'

 
    def __str__(self):
        return '<{}, {}>'.format(
            self.visibility,
            self.scope,
        )


    def __eq__(self, other):
        if (
            self.visibility == other.visibility
            and self.scope == other.scope
           ):
            return True
        return False


class Parser:
    def is_object(self, token):
        objects = ['class', 'struct']
        if token in objects:
            return True
        return False


    def is_enum(self, token):
        if token == 'enum':
            return True
        return False

 
    def is_visibility(self, token):
        visibilities = [ 'public:', 'private:', 'protected:' ]
        if token in visibilities:
            return True
        return False


    def is_literal(self, token):
        if token == 'const':
            return True
        return False

 
    def is_function(self, token):
        if token == '(':
            return True
        return False

 
    def is_duplicate_object(self, objects, potObj):
        for obj in objects:
            if obj == potObj:
                return True
        return False


    def tokenize(self, contents):
        
        whitespaces = ['\t', '\n', '\v', '\f', '\r']
        for char in whitespaces:
            contents = contents.replace(char, ' ')
        
        specialTokens = ['{', '}', '(', ')', '=']
        for char in specialTokens:
            contents = contents.replace(char, ' {} '.format(char))
       
        while '  ' in contents:
            contents = contents.replace('  ', ' ')

        contents = contents.strip()
        
        return contents.split(' ')


    def process(self, tokens):
        state_stack = []
        state_stack.append(State('none', 'global'))
        objects = []
        i = 0
        while i < len(tokens):
            print('token, {}'.format(tokens[i]))
            s = ""
            for state in state_stack:
                s = s + str(state)
            print('state_stack: {}'.format(s))
            state = state_stack[-1]
            token = tokens[i]
            if self.is_object(token):
                if state.scope == 'global' or state.scope == 'class' or state.scope == 'struct':
                    print('Appending Object: {} with state {}: '.format(tokens[i + 1], state))
                    objects.append(ObjectType(token, tokens[i + 1], copy.deepcopy(state))) 
                    if token == 'class':
                        vis = 'private:'
                    elif token == 'struct':
                        vis = 'public:'
                    print('Appending State: {}'.format(State(vis, token)))
                    state_stack.append(State(vis, token))
                    i = i + self.skip_to_token(tokens, i, '{') 
            if self.is_enum(token):
                if state.scope == 'global' or state.scope == 'class' or state.scope == 'struct':
                    objects.append(ObjectType(token, tokens[i + 1], state))
                    state_stack.append(State(state.visibility, token))
                    i = i + self.skip_to_token(tokens, i, '{')

            if self.is_visibility(token):
                state_stack[-1].visibility = token
        
            if self.is_function(token):
                obj = ObjectType('function', tokens[i - 1], copy.deepcopy(state))
                if not self.is_duplicate_object(objects, obj):
                    objects.append(obj)
                
                i = i + self.skip_to_token(tokens, i, ')')
                # Check if inline function by looking for brace
                # i + 2 required to check if static modifier included after function
                if tokens[i + 1] == '{' or tokens[i + 2] == '{':
                    # If inline function skip the entire function
                    i = i + self.skip_to_token(tokens, i, '}')
                    # Skip the last brace if not last token
                    if i != len(tokens) - 1:
                        i = i + 1

            if self.is_literal(token):
                # get variable name by looking at token before assignment
                # this is only valid since all literals must be assigned in c
                i = i + self.skip_to_token(tokens, i, '=') - 1
                objects.append(ObjectType('literal', tokens[i], copy.deepcopy(state)))

            if token == '}':
                state_stack.pop()
            
            i = i + 1

        return objects


    def filter_objects(self, objects, flags):
        # TODO: Impliment
        return objects   

     
    def skip_to_token(self, tokens, currIndex, token):
        for j in range(currIndex, len(tokens)):
            if tokens[j] == token:
                break
        return j - currIndex

    def generate_keywords(self, objects):
        keywords = [] 
        for obj in objects:
            if self.is_object(obj.objType) or self.is_enum(obj.objType):
                keywords.append(Keyword(obj.objName, 'KEYWORD1'))
            if obj.objType == 'function':
                keywords.append(Keyword(obj.objName, 'KEYWORD2'))
            if obj.objType == 'literal':
                keywords.append(Keyword(obj.objName, 'LITERAL1')) 
        return keywords

    def parse(self, fileName):
        try:
            f = open(fileName, 'r')
        except IOError as e:
            print(e)
            return

        tokens = self.tokenize(f.read())
        objects = self.process(tokens)
        objects = self.filter_objects(objects, None) 
        keywords = self.generate_keywords(objects)
        for obj in objects:
            print(obj)

        for keyword in keywords:
            print(keyword)

        self.write_keywords('KEYWORDS.txt', keywords)

        f.close()
        
    def write_keywords(self, fileName, keywords):
        try:
            f = open(fileName, 'w')
        except IOError as e:
            print(e)
            return
        
        for keyword in keywords:
            f.write('{}\n'.format(str(keyword)))

        f.close() 
