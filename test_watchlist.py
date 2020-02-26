import unittest

from app import app, db, Movie, User


class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING=True,  # 开启测试模式，出错是不会输出多余的信息
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'  # SQLite内存型数据库，不会干扰开发时使用的文件
        )
        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户一个电影信息
        user = User(name='Test', username='test')
        user.set_password('123456')
        movie = Movie(title='测试电影名称', year='2020')
        db.session.add_all([user,movie])
        db.session.commit()

        self.client = app.test_client()  # 创建测试的客户端（模拟客户端请求）
        self.runner = app.test_cli_runner()  # 创建测试命令运行期（触发自定义命令）

    def tearDown(self):
        db.session.remove()  # 清楚数据库会话
        db.drop_all()  # 删除数据库表

    # 测试程序实例app是否存在
    def test_app_exist(self):
        # 断言方法
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    # 测试404页面
    def test_404_page(self):
        response = self.client.get('/hi')  # 传入一个不存在的路由
        data = response.get_data(as_text=True)  # 获取Unicode格式的向应主体
        self.assertIn('页面跑丢了', data)
        self.assertIn('返回首页', data)
        self.assertEqual(response.status_code, 404)  # 判断响应状态码

    # 测试主页
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('测试电影名称', data)
        self.assertEqual(response.status_code, 200)

    # 登录(辅助功能，编辑，添加这些功能函数)
    def login(self):
        self.client.post('/login',data=dict(
            username = 'test',
            password = '123456'
        ),follow_redirects=True)

    # 删除
    def test_delete_item(self):
        self.login()

        response = self.client.post('/movie/delete/1',follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('删除数据成功',data)

    # 登出
    def test_logout_page(self):
        self.login()

        response = self.client.get('/logout',follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('退出登录',data)



    # 编辑
    # def test_edit_page(self):
    #     self.login()
    #
    #     response = self.client.post('/movie/edit/1',follow_redirects=True)
    #     data = response.get_data(as_text=True)
    #     self.assertIn('电影名：', data)
if __name__ == '__main__':
    unittest.main()
