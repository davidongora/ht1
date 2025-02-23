from django.contrib import admin
from .models import (AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser, AuthUserGroups, 
                     AuthUserUserPermissions, AuthtokenToken, Blogs, Coupons, DjangoAdminLog, 
                     DjangoContentType, DjangoMigrations, DjangoSession, EmailNotifications, 
                     LoyaltyPrograms, OrderItems, Orders, ProductFilters, ProductRecommendations, 
                     ProductReviews, Products, ShoppingCart, UserWishlist, Users)

# Register your models here
# admin.site.register(AuthGroup)
# admin.site.register(AuthGroupPermissions)
# admin.site.register(AuthPermission)
admin.site.register(AuthUser)
# admin.site.register(AuthUserGroups)
# admin.site.register(AuthUserUserPermissions)
# admin.site.register(AuthtokenToken)
# admin.site.register(Blogs)
# admin.site.register(Coupons)
# admin.site.register(DjangoAdminLog)
# admin.site.register(DjangoContentType)
# admin.site.register(DjangoMigrations)
# admin.site.register(DjangoSession)
# admin.site.register(EmailNotifications)
# admin.site.register(LoyaltyPrograms)
admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(ProductFilters)
admin.site.register(Products)
admin.site.register(ShoppingCart)
# admin.site.register(ProductRecommendations)
# admin.site.register(ProductReviews)
# admin.site.register(UserWishlist)
