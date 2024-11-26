import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { ApiService } from '../../api.service'; // Make sure the path is correct
import { first, Subscription } from 'rxjs';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule


@Component({
  selector: 'app-customers',
  standalone: true,
  imports: [NgFor, HttpClientModule],
  
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.css'] // Fixed typo 'styleUrl' to 'styleUrls'
})
export class CustomersComponent implements OnInit {

  images : any[] = ['NextFashion', 'FashionForAll', 'Queen clozet', 'FahionForAll',' Queen clozet']
  products: any[] = []; // List to hold fetched products
  isLoading: boolean = false;

  private unsubscribe: Subscription[] = [];

  constructor(private apiService: ApiService) {}


  ngOnInit(): void {
  }

}

