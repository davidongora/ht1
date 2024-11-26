import { NgFor } from '@angular/common';
import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-reviews',
  standalone: true,
  imports: [NgFor],
  templateUrl: './reviews.component.html',
})
export class ReviewsComponent {
  reviews = [
    { message: "Great product! Highly recommend.", author: "John Doe" },
    { message: "Fantastic customer service.", author: "Jane Smith" },
    { message: "Will definitely come back again.", author: "Alice Johnson" },
    { message: "Will definitely come back again.", author: "Alice Johnson" },

    // Add more reviews as needed
  ];


 
}
