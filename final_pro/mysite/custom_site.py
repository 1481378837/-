from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
	site_header = '大数据平台'
	site_title = '大数据管理后台'
	index_title = '首页'

custom_site = CustomSite(name='cus_admin')
