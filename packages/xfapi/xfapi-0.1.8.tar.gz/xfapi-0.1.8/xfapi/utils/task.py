"""
任务调度器，所有的定时任务都从这调度
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
task = AsyncIOScheduler(timezone="Asia/Shanghai")

task.start()