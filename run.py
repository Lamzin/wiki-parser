# -*- coding: utf-8 -*-


from wiki_parser import App


if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()
    monkey.patch_thread()

    App().run()
