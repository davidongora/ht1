import { Component } from '@angular/core';
import { HeaderComponent } from "../header/header.component";
import { FeaturesComponent } from "../../store/features/features.component";
import { CustomersComponent } from "../customers/customers.component";
import { InfoComponent } from "../info/info.component";
import { WhatWeDoComponent } from '../what-we-do/what-we-do.component';
import { ReviewsComponent } from '../reviews/reviews.component';
import { FaqsComponent } from "../faqs/faqs.component";
import { FooterComponent } from "../footer/footer.component";
import { OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { ApiService } from '../../api.service';
import { first, Subscription } from 'rxjs';
import { HttpClientModule } from '@angular/common/http';
// import { BrandsComponent } from "../brands/brands.component";
import { UsedComponent } from "../used/used.component";
import { UsedCountyComponent } from "../used-county/used-county.component";
// import { ImplementsComponent } from "../implements/implements.component";
import { ToolsComponent } from "../tools/tools.component";
import { TractorsComponent } from "../tractors/tractors.component"; // Import HttpClientModule
import { LocationsComponent } from '../locations/locations.component';
import { CartComponent } from "../cart/cart.component";
import { EmailsComponent } from "../emails/emails.component";
import { ImplementsComponent } from "../implements/implements.component";
import { SellerComponent } from "../seller/seller.component";

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [
    HeaderComponent,
    FeaturesComponent,
    CustomersComponent,
    InfoComponent,
    WhatWeDoComponent,
    ReviewsComponent,
    FaqsComponent,
    FooterComponent,
    NgFor,
    HttpClientModule // <-- Add HttpClientModule here
    ,
    // BrandsComponent,
    UsedComponent,
    UsedCountyComponent,
    // ImplementsComponent,
    ToolsComponent,
    TractorsComponent,
    LocationsComponent,
    CartComponent,
    EmailsComponent,
    ImplementsComponent,
    SellerComponent
],
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {
  images: any[] = ['image1', 'image2', 'image3', 'image4', 'image5', 'image6'];
  products: any[] = []; 
  isLoading: boolean = false;
  private unsubscribe: Subscription[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // this.ProductsList();
  }

  // ProductsList = () => {
  //   this.isLoading = true;
  //   // console.log("function initiated");

  //   const productlisting = this.apiService.getFavorites()
  //     .pipe(first())
  //     .subscribe({
  //       next: (response: any) => {
  //         this.products = response;
  //         this.products = response
  //         // console.log(this.products, 'your products');
  //       },
  //       error: (err) => {
  //         this.isLoading = false;
  //         console.log(err);
  //       }
  //     });
  //   this.unsubscribe.push(productlisting);
  // }
}
