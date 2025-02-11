from djangoplicity.test.testcases import AdminTestCase
from djangoplicity.announcements.options import AnnouncementOptions, WebUpdateOptions

class AnnouncementsTestCase(AdminTestCase):
    conf = {
        'announcements': {
            'root': '/announcements/',
            'options': AnnouncementOptions,
            'list_views': [
                ('embargo', '', 200),
                ('staging', '', 200),
                ('year', '2020/', 200),
            ]
        },
        'webupdates': {
            'root': '/announcements/webupdates/',
            'options': WebUpdateOptions,
            'list_views': []
        }
    }

    def test_index_root(self):
        for conf in list(self.conf.values()):
            response = self.client.get(conf['root'])
            self.assertEqual(response.status_code, 200)

    def test_queries(self):
        for conf in list(self.conf.values()):
            options = conf['options']
            root = conf['root']
            views = conf['list_views']

            for query, subpart, code in views:
                view_url_root = "%sarchive/%s/%s" % (root, query, subpart)
                response = self.client.get(view_url_root)
                self.assertEqual(response.status_code, code)

                for browser in getattr(options.Queries, query).browsers:
                    view_url = "%s%s/" % (view_url_root, browser)
                    response = self.client.get(view_url)
                    self.assertEqual(response.status_code, code)
