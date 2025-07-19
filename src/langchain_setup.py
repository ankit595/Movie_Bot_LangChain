# src/langchain_setup.py
from memory.swarm_memory import SwarmMemory

def init_system():
    return SwarmMemory()