import json, threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1280,'height':900})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(f'http://127.0.0.1:{server.server_port}')
        page.wait_for_function("typeof Papa !== 'undefined' && typeof Chart !== 'undefined'")
        page.wait_for_function("document.getElementById('status').textContent.startsWith('分析完成')")
        assert page.locator('#problem').input_value()=='startup'
        assert page.locator('#target').input_value()=='Profit'
        assert page.locator('#tbody tr').count()==5
        assert page.locator('#methodTabs button').count()==5
        assert page.locator('#tbody .row-badge').inner_text()=='推薦模型'
        assert page.locator('#summaryCard').is_visible()
        page.select_option('#featureCount','1')
        assert page.locator('#modelBadge').inner_text()=='自選模型'
        assert page.locator('#predictionInputs input').count()==1
        assert '1 個特徵' in page.locator('#bestFeatures').inner_text()
        assert '研發支出' in page.locator('#equation').inner_text()
        page.select_option('#featureCount','5')
        state=page.locator('#predictionInputs select')
        assert state.count()==1
        state.select_option('California')
        before=float(page.locator('#predictionValue').inner_text().replace(',',''))
        state.select_option('Florida')
        after=float(page.locator('#predictionValue').inner_text().replace(',',''))
        delta=page.evaluate("selectedModel.coefficients[selectedModel.features.indexOf('State_Florida')+1]")
        assert abs((after-before)-delta)<0.02
        page.locator('#predictionInputs input').first.fill('')
        assert page.locator('#predictionValue').inner_text()=='—'
        page.locator('#predictionInputs input').first.fill('100000')
        assert page.locator('#predictionValue').inner_text()!='—'
        page.click('#restoreBest')
        assert page.locator('#modelBadge').inner_text()=='交叉驗證推薦模型'
        assert page.locator('#featureCount').input_value()=='2'
        outputs=[]
        for problem,expected in [('startup',25),('custom',15)]:
            page.select_option('#problem',problem)
            page.click('#loadExample')
            page.wait_for_function("!document.getElementById('run').disabled")
            page.click('#run')
            page.wait_for_function("document.getElementById('status').textContent.startsWith('分析完成')",timeout=120000)
            total=0
            for button in page.locator('#methodTabs button').all():
                button.click()
                assert button.get_attribute('aria-pressed')=='true'
                assert page.locator('#methodTabs [aria-pressed="true"]').count()==1
                assert page.locator('#tbody tr').count()==expected//5
                total+=page.locator('#tbody tr').count()
                text=page.locator('#tbody').inner_text()
                assert 'NaN' not in text and 'Infinity' not in text
            assert total==expected
            page.select_option('#featureCount','1')
            assert '1 個特徵' in page.locator('#bestFeatures').inner_text()
            page.click('#restoreBest')
            outputs.append({'problem':problem,'status':page.locator('#status').inner_text(),'method':page.locator('#bestMethod').inner_text(),'rmse':page.locator('#bestRmse').inner_text()})
        page.evaluate("loadCsv('a,b\\n1,2,3\\n4,5')")
        assert page.locator('#run').is_disabled()
        page.fill('#url',f'http://127.0.0.1:{server.server_port}/data/50_Startups.csv')
        page.click('#loadUrl')
        page.wait_for_function("!document.getElementById('run').disabled")
        assert page.locator('#target').input_value()=='Profit'
        page.set_input_files('#file',{'name':'custom.csv','mimeType':'text/csv','buffer':('x,y\n'+''.join(f'{i},{2*i+3}\n' for i in range(20))).encode()})
        page.wait_for_function("document.getElementById('target').value==='y'")
        page.evaluate("loadCsv('x,y\\n'+Array.from({length:20},(_,i)=>`${i},${2*i+3}`).join('\\n'))")
        page.click('#run')
        page.wait_for_function("document.getElementById('status').textContent.startsWith('分析完成')")
        assert float(page.locator('#bestRmse').inner_text())<0.01
        page.locator('#predictionInputs input').fill('10')
        assert abs(float(page.locator('#predictionValue').inner_text())-23)<0.01
        page.locator('#predictionInputs input').fill('100')
        assert '外推' in page.locator('#predictionNote').inner_text()
        page.select_option('#problem','startup')
        assert page.locator('#run').is_disabled()
        assert page.locator('#predictionCard').is_hidden()
        page.click('#loadExample')
        page.wait_for_function("!document.getElementById('run').disabled")
        page.click('#run')
        page.wait_for_function("document.getElementById('status').textContent.startsWith('分析完成')")
        page.screenshot(path=str(ROOT/'tests/desktop.png'),full_page=True)
        page.set_viewport_size({'width':390,'height':844})
        page.wait_for_timeout(500)
        page.screenshot(path=str(ROOT/'tests/mobile.png'),full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert not errors,errors
        print(json.dumps({'passed':True,'results':outputs,'console_errors':errors},ensure_ascii=False))
        browser.close()
finally:
    server.shutdown()
