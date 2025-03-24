from django.contrib import admin
from .models import BattlePass, BattlePassTier, UserBattlePass

admin.site.register(BattlePass)
admin.site.register(BattlePassTier)
admin.site.register(UserBattlePass)