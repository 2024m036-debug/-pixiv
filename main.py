from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    # Renderがこの文字を読み取れれば「Live」になります
    return "OK"

if __name__ == "__main__":
    # Render環境では PORT 環境変数が必須です
    port = int(os.environ.get("PORT", 10000))
    # host='0.0.0.0' がないと外部（Render）から接続できません
    app.run(host='0.0.0.0', port=port)