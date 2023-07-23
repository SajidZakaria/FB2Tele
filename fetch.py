from urllib.parse import unquote
from setup_selenium import driver, goto, xpath, css_selector
try:
    from secret import *
except:
    import os
from time import sleep

def getSender():
    return driver.find_element("id", "m_story_permalink_view").find_element("tag name", "strong").get_attribute("innerText")

def getPost():
    try:
        return str(str(xpath("//meta[@property='og:image:alt']").get_attribute("content"))+"\n\n")
    except:
        return ''


def getExtras():
    images = list()
    try:
        extra = css_selector("div[data-ft='{\"tn\":\"H\"}']")
        extra_text = extra.get_attribute("innerText")
    except:
        extra_text = ''
    extra_links = driver.find_elements("xpath", "//div[@id='m_story_permalink_view']/div[1]//a[@href]")
    for link in extra_links:
        link = link.get_attribute('href')
        if 'php?u=' in link:
            link = unquote(link[link.find('=')+1:])
            extra_text += '\n<a href="'+link+'">File/Link</a>'
        elif link.startswith('https://mbasic.facebook.com/photo.php?'):
            images.append(link)

    final_images = list()
    for image in images:
        driver.get(image)
        image = xpath("//img[contains(@class, 'img') and starts-with(@src, 'https://scontent')]").get_attribute('src')
        final_images.append(image)
    return [final_images, extra_text]

def fetch(permalink):
    post = dict()
    goto('mbasic.facebook.com/groups/'+os.environ['group_link']+'/permalink/'+str(permalink))
    post['link'] = permalink
    post['sender'] = getSender() + ' [Jump To Post ↗]'
    post['text'] = getPost()
    extra = getExtras()
    post['extra'] = extra[1]
    post['image'] = extra[0]
    post['hash'] = str(hash(post['text']))
    return post
    
    
    