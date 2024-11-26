import { Component, OnInit } from '@angular/core';
import { AsyncPipe, NgFor, NgIf } from '@angular/common';
import { ApiService } from '../../api.service';
import { Observable, BehaviorSubject, combineLatest } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [NgIf, NgFor, AsyncPipe],
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.css'
})
export class CartComponent implements OnInit {
  private refreshCartTrigger = new BehaviorSubject<void>(undefined);
  public cartItems$: Observable<CartItem[]>;
  public isModalOpen: boolean = false;
  public totalPrice$: Observable<number>;

  constructor(private apiService: ApiService) {
    // Refresh cart items whenever the trigger is activated
    this.cartItems$ = this.refreshCartTrigger.pipe(
      switchMap(() => this.apiService.getCartItems())
    );

    // Calculate total price
    this.totalPrice$ = this.cartItems$.pipe(
      map(items => items.reduce((total, item) => total + (item.price * item.quantity), 0))
    );
  }

  ngOnInit(): void {
    // Initial cart items fetch
    this.refreshCartTrigger.next();
  }

  openCart(): void {
    this.isModalOpen = true;
  }

  closeCart(): void {
    this.isModalOpen = false;
  }

  // Add method to add item to cart
  addToCart(productId: string): void {
    this.apiService.addToCart(productId).subscribe({
      next: () => {
        this.refreshCartTrigger.next(); // Refresh cart after adding
      },
      error: (error) => {
        console.error('Failed to add item to cart', error);
      }
    });
  }

  removeItem(productId: string): void {
    this.apiService.removeFromCart(productId).subscribe({
      next: () => {
        this.refreshCartTrigger.next(); // Refresh cart after removing
      },
      error: (error) => {
        console.error('Failed to remove item', error);
      }
    });
  }

  updateQuantity(productId: string, event: Event): void {
    const quantity = Number((event.target as HTMLInputElement).value);
    
    if (quantity > 0) {
      this.apiService.updateCartItems(productId, quantity).subscribe({
        next: () => {
          this.refreshCartTrigger.next(); // Refresh cart after updating
        },
        error: (error) => {
          console.error('Failed to update quantity', error);
        }
      });
    }
  }
}