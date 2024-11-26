import { Injectable, OnDestroy } from '@angular/core';
import { HttpParams, HttpClient, HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class EndpointsService {

  constructor(public http: HttpClient ) {  }

  private apiUrl = 'http://127.0.0.1:8000/';  // Base API URL

  public static CART_MAIN_CONTEXT = 'cart';
  public static ORDER_ITEMS_MAIN_CONTEXT = 'order-items';
  public static ORDER_MAIN_CONTEXT = 'orders';
  public static PRODUCT_FILTERS_MAIN_CONTEXT = 'product_filters';
  public static PRODUCTS_MAIN_CONTEXT = 'products';
  public static USER_MAIN_CONTEXT = 'users';
  public static WISHLIST_MAIN_CONTEXT = 'wishlist';
  public static MESSAGING_MAIN_CONTEXT = 'messaging';
  public static TRACTORS_MAIN_CONTEXT = 'tractors';
  public static USED_TRACTORS_MAIN_CONTEXT = 'usedTractors';
  public static PAYMENT_MAIN_CONTEXT = 'payments';
  public static IMPLEMENTS_MAIN_CONTEXT = 'implements';
  public static FAVORITES_MAIN_CONTEXT = 'favorites';

  public endpoint = {
    // CART
    ADD_TO_CART: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/add/`,
    REMOVE_FROM_CART: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/remove/`,
    GET_CART_ITEMS: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/`,
    UPDATE_CART_ITEMS: `${this.apiUrl}${EndpointsService.CART_MAIN_CONTEXT}/update/`,

    // ORDERS
    CREATE_ORDER: `${this.apiUrl}${EndpointsService.ORDER_MAIN_CONTEXT}/create/`,
    GET_ORDERS: `${this.apiUrl}${EndpointsService.ORDER_MAIN_CONTEXT}/list/`,
    GET_ORDER_DETAILS: `${this.apiUrl}${EndpointsService.ORDER_MAIN_CONTEXT}/details/`,

    // USER
    LOGIN_USER: `${this.apiUrl}${EndpointsService.USER_MAIN_CONTEXT}/login/`,
    REGISTER_USER: `${this.apiUrl}${EndpointsService.USER_MAIN_CONTEXT}/register/`,
    REGISTER_SELLER: `${this.apiUrl}${EndpointsService.USER_MAIN_CONTEXT}/registerSeller/`,
    REGISTER_BUYER: `${this.apiUrl}${EndpointsService.USER_MAIN_CONTEXT}/registerBuyer/`,

    // MESSAGING
    GET_CONVERSATIONS: `${this.apiUrl}${EndpointsService.MESSAGING_MAIN_CONTEXT}/conversations/`,
    CREATE_CONVERSATION: `${this.apiUrl}${EndpointsService.MESSAGING_MAIN_CONTEXT}/chat/`,
    GET_CONVERSATION_DETAILS: `${this.apiUrl}${EndpointsService.MESSAGING_MAIN_CONTEXT}/conversations/`,
    MARK_CONVERSATION_READ: `${this.apiUrl}${EndpointsService.MESSAGING_MAIN_CONTEXT}/conversations/<int:pk>/mark-read/`,
    SEND_MESSAGE: `${this.apiUrl}${EndpointsService.MESSAGING_MAIN_CONTEXT}/messages/send/`,

    // TRACTORS
    GET_TRACTORS: `${this.apiUrl}${EndpointsService.TRACTORS_MAIN_CONTEXT}/tractors/`,
    GET_TRACTOR_DETAILS: `${this.apiUrl}${EndpointsService.TRACTORS_MAIN_CONTEXT}/tractors/<int:pk>/`,
    SEARCH_TRACTORS: `${this.apiUrl}${EndpointsService.TRACTORS_MAIN_CONTEXT}/tractors/search/`,

    // USED TRACTORS
    GET_USED_TRACTORS: `${this.apiUrl}${EndpointsService.USED_TRACTORS_MAIN_CONTEXT}/used-tractors/`,
    GET_USED_TRACTOR_DETAILS: `${this.apiUrl}${EndpointsService.USED_TRACTORS_MAIN_CONTEXT}/used-tractors/<int:pk>/`,
    SEARCH_USED_TRACTORS: `${this.apiUrl}${EndpointsService.USED_TRACTORS_MAIN_CONTEXT}/used-tractors/search/`,

    // FAVORITES
    GET_FAVORITES: `${this.apiUrl}${EndpointsService.FAVORITES_MAIN_CONTEXT}/favorites/`,
    ADD_FAVORITE: `${this.apiUrl}${EndpointsService.FAVORITES_MAIN_CONTEXT}/favorites/add/`,
    REMOVE_FAVORITE: `${this.apiUrl}${EndpointsService.FAVORITES_MAIN_CONTEXT}/favorites/<int:favorite_id>/`,

    // IMPLEMENTS
    GET_IMPLEMENT_LIST: `${this.apiUrl}${EndpointsService.IMPLEMENTS_MAIN_CONTEXT}/implements/`,
    GET_IMPLEMENT_DETAILS: `${this.apiUrl}${EndpointsService.IMPLEMENTS_MAIN_CONTEXT}/implements/<int:implement_id>/`,
    SEARCH_IMPLEMENT: `${this.apiUrl}${EndpointsService.IMPLEMENTS_MAIN_CONTEXT}/implements/search/`,

    // PAYMENTS
    MPESA_PAYMENT: `${this.apiUrl}${EndpointsService.PAYMENT_MAIN_CONTEXT}/mpesa/payment/`,
    PAYMENT_CALLBACK: `${this.apiUrl}${EndpointsService.PAYMENT_MAIN_CONTEXT}/mpepe/callback/`
  };
}
