# -*- coding: utf-8 -*-
import json
import os
import re
import socket
import threading
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

# --- 配置 ---
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-for-flask-sessions")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeMePlease123")

HOST = "0.0.0.0"
LOG_PORT = 5656
WEB_PORT = 8080

# --- 全局变量 ---
logs_data = {}
log_lock = threading.Lock()
MAX_LOGS_PER_SESSION = 500

# --- Flask & Flask-Login 设置 ---
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# --- Web 路由 ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            user = User(username)
            login_user(user)
            return redirect(url_for("index"))
        return "Invalid credentials", 401
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("logger_index.html")


# --- API 路由 ---
@app.route("/api/sessions")
@login_required
def get_sessions():
    with log_lock:
        return jsonify(sorted(logs_data.keys(), reverse=True))


@app.route("/api/logs/<session_id>")
@login_required
def get_logs_for_session(session_id):
    with log_lock:
        return jsonify(logs_data.get(session_id, []))


@app.route("/api/delete/<session_id>", methods=["POST"])
@login_required
def delete_session(session_id):
    with log_lock:
        if session_id in logs_data:
            del logs_data[session_id]
            return jsonify(status="success", message=f"Session {session_id} deleted.")
        return jsonify(status="error", message="Session not found."), 404


# --- TCP 日志接收服务 ---
def sanitize_log(log_line):
    # A simple HTML escape
    return str(log_line).replace("&", "&").replace("<", "<").replace(">", ">")


def log_receiver_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, LOG_PORT))
    server_socket.listen(10)
    print(f"[*] 日志接收服务已在 {HOST}:{LOG_PORT} 启动")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            handler_thread = threading.Thread(
                target=handle_client, args=(client_socket, addr), daemon=True
            )
            handler_thread.start()
        except Exception as e:
            print(f"[!] 接受连接时出错: {e}")


def handle_client(client_socket, addr):
    try:
        # Receive all data for the JSON payload
        data = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            data += chunk

        if not data:
            return

        payload = json.loads(data.decode("utf-8", errors="ignore"))

        session_id = payload.get("session_id")
        log_entries = payload.get("logs", [])

        if not session_id or not log_entries:
            return

        with log_lock:
            if session_id not in logs_data:
                logs_data[session_id] = []

            for log in log_entries:
                timestamp = (
                    log.get("timestamp", datetime.now().isoformat())
                    .split(".")[0]
                    .replace("T", " ")
                )
                log_type = log.get("type", "LOG")
                content = sanitize_log(log.get("content", ""))

                # Format the log entry for display
                formatted_log = f"<{timestamp}> [{log_type}] {content}"

                logs_data[session_id].append(formatted_log)

                if len(logs_data[session_id]) > MAX_LOGS_PER_SESSION:
                    logs_data[session_id] = logs_data[session_id][
                        -MAX_LOGS_PER_SESSION:
                    ]

    except json.JSONDecodeError:
        print(f"[!] Received invalid JSON from {addr[0]}")
    except ConnectionResetError:
        pass  # Client disconnected, normal
    except Exception as e:
        print(f"[!] Error processing data from {addr[0]}: {e}")
    finally:
        client_socket.close()


# --- 主程序入口 ---
if __name__ == "__main__":
    print("=" * 50)
    print("AI Challenge - Logger Service")
    print(f"Admin User: {ADMIN_USERNAME}")
    print(f"Admin Pass: {ADMIN_PASSWORD}")
    print("请务必通过环境变量或docker-compose.yml修改默认凭证!")
    print("=" * 50)
# --- 主程序入口 ---
if __name__ == '__main__':
    print("="*50)
    print("AI Challenge - Logger Service")
    print(f"Admin User: {ADMIN_USERNAME}")
    print(f"Admin Pass: {ADMIN_PASSWORD}")
    print("请务必通过环境变量或docker-compose.yml修改默认凭证!")
    print("="*50)

    receiver_thread = threading.Thread(target=log_receiver_server, daemon=True)
    receiver_thread.start()

    print(f"[*] Web 界面已在 http://{HOST}:{WEB_PORT} 启动")
    app.run(host=HOST, port=WEB_PORT)
