import mygame #　ゲーム本体をimportする

############################# 下記はpygbag用コード（固定）
import asyncio # step1

async def main(): # step2
	while 1:  	
		mygame.mainloop()
		await asyncio.sleep(0) # step3

asyncio.run(main()) # step4