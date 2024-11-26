import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { EndpointsService } from './endpoints.service'; // Import the EndpointsService

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  isLoading$: any;

  constructor(private http: HttpClient, private endpointsService: EndpointsService) { }

  // Example of API call to fetch all tractors
  public getTractors(): Observable<any> {
    return this.http.get(this.endpointsService.endpoint.GET_TRACTORS).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to fetch tractors'));
      })
    );
  }

  // Example of API call to fetch tractor details by ID
  public getTractorDetails(tractor_id: string): Observable<any> {
    const url = this.endpointsService.endpoint.GET_TRACTOR_DETAILS.replace('<int:pk>', tractor_id);
    return this.http.get(url).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to fetch tractor details'));
      })
    );
  }

  // Example of API call to search tractors
  public searchTractors(query: string): Observable<any> {
    const url = `${this.endpointsService.endpoint.SEARCH_TRACTORS}?search=${query}`;
    return this.http.get(url).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to search tractors'));
      })
    );
  }

  // Example of API call to get all favorites
  public getFavorites(): Observable<any> {
    return this.http.get(this.endpointsService.endpoint.GET_FAVORITES).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to fetch favorites'));
      })
    );
  }

  // Example of API call to add a favorite
  public addFavorite(favoriteData: any): Observable<any> {
    return this.http.post(this.endpointsService.endpoint.ADD_FAVORITE, favoriteData).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to add favorite'));
      })
    );
  }

  // Example of API call to remove a favorite
  public removeFavorite(favoriteId: string): Observable<any> {
    const url = this.endpointsService.endpoint.REMOVE_FAVORITE.replace('<int:favorite_id>', favoriteId);
    return this.http.delete(url).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to remove favorite'));
      })
    );
  }

  // Example of API call to create an order
  public createOrder(orderData: any): Observable<any> {
    return this.http.post(this.endpointsService.endpoint.CREATE_ORDER, orderData).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to create order'));
      })
    );
  }

  // Example of API call to fetch all orders
  public getOrders(): Observable<any> {
    return this.http.get(this.endpointsService.endpoint.GET_ORDERS).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to fetch orders'));
      })
    );
  }

  // Example of API call to get order details
  public getOrderDetails(order_id: string): Observable<any> {
    const url = this.endpointsService.endpoint.GET_ORDER_DETAILS.replace('<int:pk>', order_id);
    return this.http.get(url).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to fetch order details'));
      })
    );
  }

  // Example of API call for user login
  public loginUser(credentials: any): Observable<any> {
    return this.http.post(this.endpointsService.endpoint.LOGIN_USER, credentials).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Login failed'));
      })
    );
  }

  // Example of API call for user registration
  public registerUser(userData: any): Observable<any> {
    return this.http.post(this.endpointsService.endpoint.REGISTER_USER, userData).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Registration failed'));
      })
    );
  }

  // Example of API call for sending a message
  public sendMessage(messageData: any): Observable<any> {
    return this.http.post(this.endpointsService.endpoint.SEND_MESSAGE, messageData).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to send message'));
      })
    );
  }

  // Add item to cart
  public addToCart(productId: string): Observable<any> {
    const url = this.endpointsService.endpoint.ADD_TO_CART + productId;
    return this.http.post(url, {}).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to add item to cart'));
      })
    );
  }

  // Remove item from cart
  public removeFromCart(productId: string): Observable<any> {
    const url = this.endpointsService.endpoint.REMOVE_FROM_CART + productId;
    return this.http.delete(url).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to remove item from cart'));
      })
    );
  }

  // Get cart items
  public getCartItems(): Observable<any> {
    const url = this.endpointsService.endpoint.GET_CART_ITEMS;
    return this.http.get(url).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to fetch cart items'));
      })
    );
  }

  // Update cart item quantity
  public updateCartItems(productId: string, quantity: number): Observable<any> {
    const url = this.endpointsService.endpoint.UPDATE_CART_ITEMS + productId;
    return this.http.put(url, { quantity }).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        return throwError(() => new Error('Failed to update cart item'));
      })
    );
  }

}
