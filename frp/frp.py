import requests
from pyquery import PyQuery as pq
import urllib3
import os
from database.database import Session
from datetime import datetime
from database.models import FrpRelease, FrpAssets

os.environ.setdefault('REQUESTS_CA_BUNDLE', '')
os.environ.setdefault('CURL_CA_BUNDLE', '')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Frp():
    git = 'https://github.com/fatedier/frp.git'
    releases_url = 'https://github.com/fatedier/frp/releases'
    assets_url = 'https://github.com/fatedier/frp/releases/expanded_assets/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def __init__(self):
        self.s = requests.Session()

    def get_releases(self, page=1):
        params = {
            'page': page
        }
        r = self.s.get(self.releases_url, headers=self.headers,
                       params=params, verify=False)
        if r.status_code == 200:
            doc = pq(r.text)
            section_list = doc('section')
            data = []
            for val in section_list.items():
                releas = val.find('.Link--primary').text()
                release_time = val.find('relative-time').attr('datetime')
                release_time = release_time.replace('T', ' ')
                release_time = release_time.replace('Z', '')
                octicon = val.find('.Link--muted code').text()
                tag = val.find('.css-truncate-target').text()
                # print(tag)
                text = val.find('.markdown-body').html()
                # print(val.find('.markdown-body').text())
                temp = list(tag)
                version = ''
                for k in temp:
                    if k.isnumeric():
                        version = version + k
                data.append({
                    'releas': releas,
                    'release_time': release_time,
                    'octicon': octicon,
                    'tag': tag,
                    'text': text,
                    'version': int(version),
                })
            # print(section_list.length)
            # last_page = doc('.pagination').find('.next_page').children()
            return data

    def get_assets(self, tag):
        r = self.s.get(self.assets_url + tag,
                       headers=self.headers, verify=False)
        if r.status_code == 200:
            doc = pq(r.text)
            li_list = doc('li')
            data = []
            for li in li_list.items():
                filename = li.find('.Truncate').text()
                # print(filename)
                if filename[0:3] == 'frp':
                    name = filename.split('_')
                    software = name[0]
                    edition = name[1]
                    system = name[2]
                    if len(name) == 4:
                        machine = name[3][:name[3].find('.')]
                        format = name[3][name[3].find('.') + 1:]
                    else:
                        machine = ''
                        format = name[2][name[2].find('.') + 1:]
                else:
                    software = ''
                    edition = ''
                    system = ''
                    machine = ''
                    format = filename[filename.rfind('.') + 1:]
                url = 'https://github.com/' + li.find('.Truncate').attr('href')
                filesize = li.find('.flex-justify-end .text-sm-left').text()
                # print(filesize)
                release_time = li.find(
                    '.flex-justify-end relative-time').attr('datetime')
                release_time = release_time.replace('T', ' ')
                release_time = release_time.replace('Z', '')
                # print(release_time)
                data.append({
                    'tag':tag,
                    'software':software,
                    'edition':edition,
                    'system':system,
                    'machine':machine,
                    'format':format,
                    'url':url,
                    'filename':filename,
                    'filesize':filesize,
                    'release_time':release_time,
                })
            return data
        
    def update_frp(self):
        frp = self
        page = 1
        while True:
            releases_list = frp.get_releases(page)
            print('当前页数', page)
            if len(releases_list) == 0:
                break
            print('releases_list_count', len(releases_list))
            for releas in releases_list:
                releas_info = Session.query(FrpRelease).filter(
                    FrpRelease.tag == releas['tag'], FrpRelease.releas == releas['releas']).first()
                releas_id = None
                tag = releas['tag']
                if releas_info is None:
                    releas_obj = FrpRelease(
                        tag=releas['tag'],
                        releas=releas['releas'],
                        text=releas['text'],
                        version=releas['version'],
                        release_time=datetime.strptime(
                            releas['release_time'], '%Y-%m-%d %H:%M:%S'),
                    )
                    Session.add(releas_obj)
                    Session.commit()
                    print(releas_obj.id)
                    releas_id = releas_obj.id
                    continue
                else:
                    releas_info.text = releas['text']
                    releas_info.version = releas['version']
                    releas_info.release_time = datetime.strptime(
                        releas['release_time'], '%Y-%m-%d %H:%M:%S')
                    releas_id = releas_info.id

                add_tags = []
                tag_list = frp.get_assets(tag)
                print('tag_list_count', len(tag_list))
                print('当前版本', tag)
                for tag_data in tag_list:
                    # print('tag_data', tag_data['filename'])
                    tag_info = Session.query(FrpAssets).filter(
                        FrpAssets.tag == tag_data['tag']).first()
                    if tag_info is None:
                        tag_obj = FrpAssets(
                            releas_id=releas_id,
                            tag=tag_data['tag'],
                            filename=tag_data['filename'],
                            software=tag_data['software'],
                            edition=tag_data['edition'],
                            system=tag_data['system'],
                            machine=tag_data['machine'],
                            format=tag_data['format'],
                            url=tag_data['url'],
                            filesize=tag_data['filesize'],
                            release_time=datetime.strptime(
                                tag_data['release_time'], '%Y-%m-%d %H:%M:%S'),
                        )
                        add_tags.append(tag_obj)
                    else:
                        tag_info.filename = tag_data['filename']
                        tag_info.software = tag_data['software']
                        tag_info.edition = tag_data['edition']
                        tag_info.system = tag_data['system']
                        tag_info.machine = tag_data['machine']
                        tag_info.format = tag_data['format']
                        tag_info.url = tag_data['url']
                        tag_info.filesize = tag_data['filesize']
                        tag_info.release_time = datetime.strptime(
                            tag_data['release_time'], '%Y-%m-%d %H:%M:%S')
                if len(add_tags) > 0:
                    Session.add_all(add_tags)
                    Session.commit()
            page = page + 1