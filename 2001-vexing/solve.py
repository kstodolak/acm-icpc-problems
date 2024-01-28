#!/usr/bin/python3
import os
from collections import deque

def print_map(M):
  [print(line) for line in M]
  print('-----------------------')

def fall_down(M, y, x):
  if M[y+1][x] == '-':
    return fall_down(M, y+1, x)
  else:
    return (y, x)

def gravity(M):
  moved = 0
  for y in range(len(M)-1, 0-1, -1):
    for x in range(len(M[y])): 
      c = M[y][x]
      if c.isalnum():
        (yy, xx) = fall_down(M, y, x)
        if (yy, xx) == (y, x): continue
        moved += 1
        M[yy][xx] = c
        M[y][x] = '-'
  return moved
  
def remove(M):
  blocks = set()
  
  for y in range(len(M)):
    for x in range(len(M[y])):
      c = M[y][x]
      if c.isalnum():
        blocks.add((y, x))

  to_remove = set()
  for (y, x) in blocks:
    c = M[y][x]
    for (dy, dx) in [(1,0), (-1, 0), (0, 1), (0, -1)]:
      yy = y + dy
      xx = x + dx
      if (yy, xx) in blocks and M[yy][xx] == c:
        to_remove.add((y, x))
        break
  
  for (y, x) in to_remove:
    M[y][x] = '-'
  
  return len(blocks) - len(to_remove)

def copy(M):
  new_M = []
  for line in M:
    row = []
    for c in line:
      row.append(c)
    new_M.append(row)
  return new_M

def get_hash(M):
  result = ''
  for line in M:
    for c in line:
      result += c
  return result

def get_todo(M):
  todo = []
  for y in range(len(M)):
    for x in range(len(M[y])):
      c = M[y][x]
      if not c.isalnum(): continue # not a block
      for dx in [1, -1]:
        xx = x + dx
        if M[y][xx] == '-': 
          todo.append(((y, x), (y, xx)))
  
  return todo

def solve2(M):
  todo = deque([(M, 1)])
  visited = set()

  while todo:
    curr, moves = todo.popleft()
    assert moves <= 11
    curr_hash = get_hash(curr)
    if curr_hash in visited:
      continue
    visited.add(curr_hash)
    possible_moves = get_todo(curr)
    for moved_from, moved_to in possible_moves:
      new_M = copy(curr)
      y, x = moved_from
      c = new_M[y][x]
      yy, xx = moved_to
      new_M[yy][xx] = c
      new_M[y][x] = '-'
      gravity(new_M)
      while True:
        left = remove(new_M)
        if left == 0: return moves 
        moved = gravity(new_M)
        if moved == 0:
          break
      todo.append((new_M, moves + 1))

    
f = open(os.path.dirname(__file__) + '/in')
lines = f.read().splitlines()
MAP = None

for i in range(len(lines)):
  line = lines[i]
  if line[0].isnumeric():
    if MAP != None:
      print_map(MAP)
      print(solve2(MAP))
    MAP = []
  else:
    row = []
    for c in line:
      row.append(c)
    MAP.append(row)