import { NgFor } from '@angular/common';
// import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../api.service'; // Ensure the path is correct
import { Component, OnInit, TemplateRef } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
// import { ApiService } from '../../api.service'; // Ensure the path is correct
import { catchError, first, Subscription, throwError } from 'rxjs';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
// import { NgFor, NgIf } from '@angular/common';
// import { FilterComponent } from '../filter/filter.component';
@Component({
  selector: 'app-filter',
  standalone: true,
  imports: [NgFor, FormsModule ],
  templateUrl: './filter.component.html',
  styleUrl: './filter.component.css'
})
export class FilterComponent {


  public gender: any[] = ['Male', 'Female']
  public AgeGroup: any[] = ['Adult', 'Children']
  public price: number = 50; 
  public size: any[] = ['Small', 'Medium', 'Large']

  constructor(private apiService: ApiService) {}

  public products: any[] = []
  productslist = () => {
    console.log("Fetching products...");

    this.apiService.getTractors()
      .pipe(
        first(),
        catchError(err => {
          console.error('Failed to fetch products', err);
          return throwError(() => new Error('Failed to fetch products'));
        })
      )
      .subscribe({
        next: (response: any) => {
          this.products = response;
        },
        error: (err) => {
          err.errorMessage = 'Failed to fetch products. Please try again later.';
        }
      });
}
}
