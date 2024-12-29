# 项目说明

- ...

# 更新历史

- 加入爬虫案例

# 爬虫案列

## 爬取皮肤图片

### 代码

```python

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor

from loguru import logger

from craws import AirSpider


class WZRYSkinSpider(AirSpider):
    def parse_url(self, url, b=False):
        try:
            res = self.get(url)
            res.encoding = "GBK"
            assert res.status_code == 200, "Code not is 200"
            return res.content if b else res.text
        except:
            pass

    def download_img(self, img_url, hero_name, hero_img, num):
        b_data = self.parse_url(img_url, b=True)
        if b_data is None:
            return
        with open(hero_img, "wb") as f:
            f.write(b_data)
        logger.success(f"{hero_name} 第{num}张皮肤图片 下载完毕")

    def process_hero(self, hero_id, name):
        logger.info(f"{hero_id}\t{name}\t处理中...")

        hero_dir = f"./英雄皮肤/{name}"
        if not os.path.exists(hero_dir):
            os.makedirs(hero_dir, exist_ok=True)

        with ThreadPoolExecutor(max_workers=20) as pool:
            for num in range(1, 20):
                hero_img = f"{hero_dir}/皮肤_{num}.png"
                if os.path.exists(hero_img):
                    logger.warning(f"{hero_img}已下载过，跳过")
                    continue
                img_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{hero_id}/{hero_id}-bigskin-{num}.jpg"
                pool.submit(self.download_img, img_url, name, hero_img, num)

    def crawl(self):
        api_url = "https://game.gtimg.cn/images/yxzj/web201706/js/heroid.js"
        text = self.parse_url(api_url)
        search_result = re.search('var module_exports = ({.*?})', text, re.S)
        hero_info_str = search_result.group(1)
        hero_info_str = re.sub("'", '"', hero_info_str)
        hero_info_dict = json.loads(hero_info_str)

        with ThreadPoolExecutor(max_workers=10) as pool:
            for hero in hero_info_dict:
                name, id = hero_info_dict[hero], hero
                pool.submit(self.process_hero, id, name)


if __name__ == '__main__':
    WZRYSkinSpider().crawl()

```