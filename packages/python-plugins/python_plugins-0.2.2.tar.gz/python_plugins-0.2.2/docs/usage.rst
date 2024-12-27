=====
Usage
=====

.. _installation:

Installation
==============

Install and update using pip:

.. code-block:: console

   (.venv) $ pip install -U python-plugins

email
======

.. code-block:: python
   
   # smtp's host
   host = "smtp.host"
   port = "465"
   # smtp's username and password
   user = "test@test.com"
   password = "your password"

   # receiver and subject and content
   to = "test2@test.com"
   data = {
      "to": to,
      "subject": "subject of msg",
      "content": "content of msg",
   }

   s = SmtpSSL(host, port, user, password)
   r = s.send_emsg(data)

mixins
======

.. code-block:: python

   from flask_sqlalchemy import SQLAlchemy
   from sqlalchemy.orm import DeclarativeBase
   
   from python_plugins.models.mixins import PrimaryKeyMixin
   from python_plugins.models.mixins import UserMixin
   from python_plugins.models.mixins import DataMixin
   from python_plugins.models.mixins import TimestampMixin

   class Base(DeclarativeBase):
      pass

   db = SQLAlchemy(model_class=Base)

   class User(db.Model,PrimaryKeyMixin, DataMixin, TimestampMixin, UserMixin):
      __tablename__ = "users"

walk_remove_dir
=======================

.. code-block:: python

    from  python_plugins.utils import remove,remove_pycache,remove_ipynb_checkpoints

    remove_pycache()   # default is "."
    remove_pycache("./tests")

    remove(dir,rm_dir_name)


encrypt,decrypt
================

.. code-block:: python

    from python_plugins.crypto import encrypt_txtfile,decrypt_txtfile

    # encrypt
    encrypt_txtfile(txtfile)
    encrypt_txtfile(txtfile,".")
    encrypt_txtfile(txtfile, newfile, password=password)
    
    # decrypt
    decrypt_txtfile(encryptedfile)
    decrypt_txtfile(encryptedfile,".")
    decrypt_txtfile(encryptedfile, srcfile, password=password)     


weixin.wechat
==================

.. code-block:: python

   from python_plugins.weixin.wechat import Wechat

   class MyWechat(Wechat):
      def get_app(self) -> dict:
         # may depended on self.name from self.__init__(name)
         return "<your app>"

   mywechat = MyWechat("name")
   mywechat.verify(query)
   mywechat.chat(query,content)
   
