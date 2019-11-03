#!/usr/bin/python3

import os
import re
import copy


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


class Parser:
    def is_object(self, token):
        objects = ['class', 'struct']
        if token in objects:
            return token
        return None

    def is_enum(self, token):
        if token == 'enum':
            return token
        return None

    
    def is_visibility(self, token):
        visibilities = ['public:', 'private:', 'protected:']
        if token in visibilities:
            return token
        return None


    def tokenize(self, f):
        contents = f.read()
        
        whitespaces = ['\t', '\n', '\v', '\f', '\r']
        for char in whitespaces:
            contents = contents.replace(char, ' ')
        
        while '  ' in contents:
            contents = contents.replace('  ', ' ')

        contents = contents.strip()
        
        return contents.split(' ')


    def process(self, tokens):
        state_stack = []
        state_stack.append(State('none', 'global'))
        objects = []
        for i in range(len(tokens)):
            print('token, {}'.format(tokens[i]))
            s = ""
            for state in state_stack:
                s = s + str(state)
            print('state_stack: {}'.format(s))
            state = state_stack[-1]
            token = tokens[i]
            obj = self.is_object(token)
            enum = self.is_enum(token)
            visibility = self.is_visibility(token)
            if obj:
                if state.scope == 'global' or state.scope == 'class' or state.scope == 'struct':
                    print('Appending Object: {} with state {}: '.format(tokens[i + 1], state))
                    objects.append(ObjectType(token, tokens[i + 1], copy.deepcopy(state))) 
                    if obj == 'class':
                        vis = 'private:'
                    elif obj == 'struct':
                        vis = 'public:'
                    print('Appending State: {}'.format(State(vis, obj)))
                    state_stack.append(State(vis, obj))
                    i = self.skip_to_token(tokens, i, '{')  
            if enum:
                if state.scope == 'global' or state.scope == 'class' or state.scope == 'struct':
                    objects.append(ObjectType(token, tokens[i + 1], state))
                    state_stack.append(State(state.visibility, enum))
                    i = self.skip_to_token(tokens, i, '{')
            if visibility:
                state_stack[-1].visibility = visibility 

            if token == '}' or token == '};':
                state_stack.pop()

        for obj in objects:
            print(obj)

    
    def skip_to_token(self, tokens, currIndex, token):
        for j in range(currIndex, len(tokens)):
            if tokens[j] == token:
                break
        return j - currIndex


    def parse(self, fileName):
        try:
            f = open(fileName, 'r')
        except IOError as e:
            print(e)
            return
        
        tokens = self.tokenize(f)
        print('Tokens: ')
        print('-------------------------------------------')
        print(tokens)
        self.process(tokens) 




        
