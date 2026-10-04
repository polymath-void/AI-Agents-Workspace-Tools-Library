#!/data/data/com.termux/files/usr/bin/env bash

# gemini_session_mgr.sh - Upgraded session profile manager for gemini-cli

CONFIG_BASE="$HOME/.gemini"
SESSION_DIR="$HOME/.gemini_sessions"
PERSISTENCE_DIR="$HOME/.gemini_persistence"

mkdir -p "$SESSION_DIR" "$PERSISTENCE_DIR"

usage() {
    echo "Usage: gemini_session_mgr [create|switch|list] [profile_name]"
}

persist_context() {
    # Save essential context to be reloaded
    if [ -d "$CONFIG_BASE" ]; then
        cp "$CONFIG_BASE/projects.json" "$PERSISTENCE_DIR/last_context.json" 2>/dev/null
        # Save active agent identifiers or state pointers if they exist
        [ -f "$CONFIG_BASE/state.json" ] && cp "$CONFIG_BASE/state.json" "$PERSISTENCE_DIR/last_state.json"
    fi
}

restore_context() {
    # Restore context to the newly active config
    if [ -f "$PERSISTENCE_DIR/last_context.json" ]; then
        cp "$PERSISTENCE_DIR/last_context.json" "$CONFIG_BASE/projects.json"
    fi
    if [ -f "$PERSISTENCE_DIR/last_state.json" ]; then
        cp "$PERSISTENCE_DIR/last_state.json" "$CONFIG_BASE/state.json"
    fi
}

case "$1" in
    create)
        if [ -z "$2" ]; then usage; exit 1; fi
        mkdir -p "$SESSION_DIR/$2"
        # Ensure standard subdirectories exist
        mkdir -p "$SESSION_DIR/$2/agents" "$SESSION_DIR/$2/history"
        echo "Created profile: $2"
        ;;
    switch)
        if [ -z "$2" ]; then usage; exit 1; fi
        if [ ! -d "$SESSION_DIR/$2" ]; then echo "Profile not found."; exit 1; fi
        
        # 1. Persist current context
        persist_context
        
        # 2. Unlink current, swap to new
        rm -f "$CONFIG_BASE"
        ln -s "$SESSION_DIR/$2" "$CONFIG_BASE"
        
        # 3. Restore persisted context
        restore_context
        
        echo "Switched to profile: $2 with context preserved."
        ;;
    list)
        ls "$SESSION_DIR"
        ;;
    *)
        usage
        ;;
esac
