from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/verify')
def code():
    try:
        code_ = request.args.get("code") # verify?code=123 에서 123을 가져오는 변수

        if not code_:
            return render_template('error.html', title="접속 오류",dec=f"코드를 입력 해 주세요.")
        else:
            w = open("code.txt","w")
            w.write(code_)
            w.close()
            print("success")
            return render_template('success.html', verify_code=code_)
    except Exception as e:
        return render_template('error.html', dec=f"Internal Server Error: {e}")

    
@app.route('/')
def main():
    return render_template ('error.html',dec="올바른 주소를 입력 해 주세요.")



if __name__ == "__main__":
    try:
        app.run(host='127.0.0.1', port=80)
    except Exception as e:
        pass