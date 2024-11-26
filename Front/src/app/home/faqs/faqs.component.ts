import { NgFor, NgIf } from '@angular/common';
import { Component } from '@angular/core';


@Component({
  selector: 'app-faqs',
  standalone: true,
  imports: [NgFor, NgIf],
  templateUrl: './faqs.component.html',
  styleUrl: './faqs.component.css'
})
export class FaqsComponent {
  
  faqs = [
    { question: "What payment methods are available?", answer: "We accept credit cards, debit cards, and PayPal for your convenience.", show: false },
  { question: "How can I track my order?", answer: "You can track your order using the tracking link sent to your email after the order is shipped.", show: false },
  { question: "What is the return policy?", answer: "You can return most items within 30 days of purchase for a full refund, provided they are in original condition.", show: false },
  { question: "How do I create an account?", answer: "You can create an account by clicking on the 'Sign Up' button and filling in your details.", show: false },
  { question: "Can I change or cancel my order?", answer: "You can change or cancel your order within 24 hours of placing it by contacting customer support.", show: false }
    ];

  toggleFAQ(index: number): void {
    this.faqs[index].show = !this.faqs[index].show;
  }

}
