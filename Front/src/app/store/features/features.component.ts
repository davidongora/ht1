import { Component, OnInit, TemplateRef } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ApiService } from '../../api.service'; // Ensure the path is correct
import { catchError, first, Subscription, throwError } from 'rxjs';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { NgClass, NgFor, NgIf } from '@angular/common';
import { FilterComponent } from '../filter/filter.component';
// import { catchError, throwError } from 'rxjs';
import { interval } from 'rxjs';


@Component({
  selector: 'app-features',
  standalone: true,
  imports: [FilterComponent, NgFor, NgIf, MatDialogModule, MatButtonModule, NgClass],
  templateUrl: './features.component.html',
  styleUrls: ['./features.component.css'] // Ensure the styleUrl is correct
})
export class FeaturesComponent implements OnInit {
  products: any[] = []; 
  isLoading: boolean = true;

  private unsubscribe: Subscription[] = [];
  pageSize = 9; 
  currentPage = 1;
  pagedProducts: any[] = [];

  constructor(private apiService: ApiService, public dialog: MatDialog) {}

  ngOnInit(): void {
    // this.apiService.isLoading$.subscribe(isLoading => {
    //   this.isLoading = isLoading; 
    // });
  
    this.productslist(); 

    interval(3000000)
      .subscribe(() => {
        this.productslist(true);
      })
  }

  productslist = ( forceFetch =false) => {
    this.isLoading = true;
    console.log("Fetching products...");
    const storedProducts = localStorage.getItem('products');

    if (storedProducts) {
      this.products = JSON.parse(storedProducts);
      this.updatePagedProducts()
      this.isLoading = false;
      return;
    }

    if (!forceFetch) {
      const storedProducts = localStorage.getItem('products');
      if (storedProducts) {
        this.products = JSON.parse(storedProducts);
        this.updatePagedProducts();
        this.isLoading = false;
        return;
      }
    }

    this.apiService.getTractors()
      .pipe(
        first(),
        catchError(err => {
          this.isLoading = false;
          console.error('Failed to fetch products', err);
          return throwError(() => new Error('Failed to fetch products'));
        })
      )
      .subscribe({
        next: (response: any) => {
          this.products = response;
          localStorage.setItem('products', JSON.stringify(response))
          this.updatePagedProducts();
          this.isLoading = false;
        },
        error: (err) => {
          // Handle any additional errors if needed
          // return of ([]);
          err.errorMessage = 'Failed to fetch products. Please try again later.';

        }
      });
}

  updatePagedProducts() {
    const startIndex = (this.currentPage - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    this.pagedProducts = this.products.slice(startIndex, endIndex);
  }

  changePage(page: number) {
    this.currentPage = page;
    this.updatePagedProducts();
  }

  get totalPages() {
    return Math.ceil(this.products.length / this.pageSize);
  }

  openDialog(templateRef: TemplateRef<any>, item: any): void {
    this.dialog.open(templateRef, {
      // data: item, // Passing selected product data to the modal
      // width: '600px',
      // height: '500px',
      // panelClass: 'custom-dialog-container'
    });
  }
  

  closeDialog(): void {
    this.dialog.closeAll(); // Close all dialogs
  }
  activeTab: string = 'popular'; // default tab
  // isLoading: boolean = false;
  // totalPages: number = 5;

  // Product data for each tab
  popularProducts = [
    { name: 'Mahindra 575 DI XP Plus', imageUrl: '../../../assets/car.png', hp: 47, cc: 2979 },
    { name: 'Sonalika 42 DI Sikander', imageUrl: '../../../assets/car.png', hp: 42, cc: 2891 }
    // Add more products as needed
  ];

  latestProducts = [
    { name: 'Sonalika 42 DI Sikander', imageUrl: '../../../assets/car.png', hp: 42, cc: 2891 },
    { name: 'Mahindra 275 DI XP Plus', imageUrl: '../../../assets/car.png', hp: 37, cc: 2235 }
    // Add more products as needed
  ];

  upcomingProducts = [
    { name: 'Mahindra 275 DI XP Plus', imageUrl: '../../../assets/car.png', hp: 37, cc: 2235 },
    { name: 'Mahindra 375 DI XP Plus', imageUrl: '../../../assets/car.png', hp: 40, cc: 2500 }
    // Add more products as needed
  ];

}
