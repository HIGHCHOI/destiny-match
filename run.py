from app import create_app
#from app.models import init_db
from flask import current_app

app = create_app()

# 앱 시작 시 DB가 없다면 초기화 (개발 처음만 실행)
# with app.app_context():
#    init_db()

if __name__ == '__main__':
    app.run(debug=True)
