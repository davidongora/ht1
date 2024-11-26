import { Component, inject, TemplateRef } from '@angular/core';
import { NgForm } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar'; // Import MatSnackBar
import { ApiService } from '../../api.service';
import { first, catchError, map, switchMap } from 'rxjs/operators';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import "driver.js/dist/driver.css";
import { FormsModule } from '@angular/forms';
// import { TranslateService } from '@ngx-translate/core';
import { Inject } from '@angular/core';

// const driverObj = driver({
//   showProgress: true,
//   animate: true,  
//   doneBtnText: 'Finish', 
//   nextBtnText: 'Next',  
//   prevBtnText: 'Previous',  

//   steps: [
//     // { element: '#title', popover: { title: 'FashionForAll', description: 'Description' } },
//     { element: '#orders', popover: { title: 'orders', description: 'Description' } },
//     { element: '#contact', popover: { title: 'contact', description: 'Description' } },
//     { element: '#title', popover: { title: 'FashionForAll', description: 'Description' } },
//   ]
// });

// driverObj.drive();


interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
  ],
})


export class HeaderComponent {
checkout() {
throw new Error('Method not implemented.');
}


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
  
  isLoading = false;

  // constructor(@Inject(TranslateService) private translate: TranslateService) {
  //   this.translate.setDefaultLang('en');
  // }

  newTractorItems = ['All Tractors', 'Popular Tractors', 'Upcoming Tractors', 'Latest Tractors', 'Electric Tractors', 'Mini Tractors'];
  buyUsedItems = ['Certified Used Tractors', 'Used Tractors', 'Used Mini Tractors', 'Used Farm Implements', 'Used Harvester', 'Tractor Valuation', 'Find Used Tractor'];
  sellUsedItems = ['Used Tractor', 'Used Farm Implements', 'Used Harvester'];
  farmEquipmentItems = ['Implements', 'All Harvester', 'Mini Harvester'];
  showroomItems = ['FMD', 'Sichey', 'CFAO', 'Mascor', 'CMC', 'Terranova', 'All Showroom'];
  loanItems = ['New Tractor Loan', 'Used Tractor Loan', 'Loan Against Tractor', 'Personal Loan'];
  moreItems = ['News & Updates', 'All News', 'Tractor News', 'Agriculture News', 'Sarkari Yojana News', 'Web Story', 'Blog', 'Videos'];

// Search variables for each dropdown
newTractorSearch = '';
buyUsedSearch = '';
sellUsedSearch = '';
farmEquipmentSearch = '';
showroomSearch = '';
loanSearch = '';
moreSearch = '';

switchLanguage(language: string) {
  // this.translate.use(language); // Change language dynamically
}

// Filter method to handle search functionality
filterItems(items: string[], searchQuery: string) {
  if (!searchQuery) {
    return items;
  }
  return items.filter(item => item.toLowerCase().includes(searchQuery.toLowerCase()));
}
  // Inject services using Angular's inject method for standalone components
  // private apiService = inject(ApiService);
  private dialog = inject(MatDialog);
  private snackBar = inject(MatSnackBar); // Inject MatSnackBar

  // Method to open the dialog using the click event to get the position
  openDialog(event: MouseEvent, templateRef: TemplateRef<any>): void {
    const dialogPosition = {
      top: `${event.clientY}px`,
      left: `${event.clientX}px`
    };

    this.dialog.open(templateRef, {
      // width: '300px', // Customize modal width
      // position: dialogPosition, // Set position next to where it was clicked
    });
  }

  // Method to close the dialog from within the modal
  closeDialog(dialogRef: MatDialogRef<any>): void {
    dialogRef.close();
  }

  // Show toast messages
  private showToast(message: string, action: string = 'Close') {
    this.snackBar.open(message, action, {
      duration: 3000, // Duration in milliseconds
      horizontalPosition: 'right', // Toast position
      verticalPosition: 'top', // Toast position
    });
  }

  

  // Register method handler
onRegister(signupForm: NgForm, dialogRef: MatDialogRef<any>) {
  if (!signupForm.valid) {
    return;
  }

  const { first_name, last_name, email, password, number } = signupForm.value;
  this.isLoading = true;

  // Register service worker and request permission for push notifications
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    navigator.serviceWorker.register('/service-worker.js').then(registration => {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: this.urlBase64ToUint8Array('BKL0DcVViUJXNlPcmloYUzrvdrqm9cf7XzPrnED3c2oz_GRk3Zgn3u6MNwwRJVL4-P7-xe4UglvAnfE6wK8JGQM') // Replace with your VAPID public key
          }).then(subscription => {
            const pushSubscription = JSON.stringify(subscription);

            // Proceed with user registration along with the subscription data
            this.apiService.registerUser(first_name)
              .pipe(
                first(),
                catchError((error: HttpErrorResponse) => {
                  this.isLoading = false;
                  console.error('Registration failed', error);
                  this.showToast('Failed to register user. Please try again.');
                  return throwError(() => new Error('Failed to register user'));
                })
              )
              .subscribe({
                next: (response: any) => {
                  console.log('Registration successful', response);
                  this.isLoading = false;
                  this.showToast('Registration successful!');
                  this.closeDialog(dialogRef);
                },
                error: (err) => {
                  console.error('Registration error:', err);
                  this.isLoading = false;
                  this.showToast('Registration error. Please try again.');
                }
              });
          }).catch(error => {
            console.error('Push subscription failed:', error);
            this.isLoading = false;
            this.showToast('Push subscription failed. Please try again.');
          });
        } else {
          this.isLoading = false;
          this.showToast('Push notifications permission denied.');
        }
      });
    }).catch(error => {
      console.error('Service worker registration failed:', error);
      this.isLoading = false;
      this.showToast('Service worker registration failed. Please try again.');
    });
  } else {
    this.isLoading = false;
    this.showToast('Push notifications are not supported in your browser.');
  }
}

// Helper function to convert the VAPID public key to Uint8Array
private urlBase64ToUint8Array(base64String: string) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}


  // Login method handler
  onLogin(loginForm: NgForm, dialogRef: MatDialogRef<any>) {
    if (!loginForm.valid) {
      return;
    }

    const { email, password } = loginForm.value;
    this.isLoading = true;

    this.apiService.loginUser(email)
      .pipe(
        first(),
        catchError((error: HttpErrorResponse) => {
          this.isLoading = false;
          console.error('Login failed', error);
          this.showToast('Failed to login. Please try again.');
          return throwError(() => new Error('Failed to login'));
        })
      )
      .subscribe({
        next: (response: any) => {
          console.log('Login successful', response);
          this.isLoading = false;
          this.showToast('Login successful!');
          this.closeDialog(dialogRef);
        },
        error: (err) => {
          console.error('Login error:', err);
          this.isLoading = false;
          this.showToast('Login error. Please try again.');
        }
      });
  }
}
