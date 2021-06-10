# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Car Repair and Automotive Service Maintenance Management Odoo App",
    "version" : "14.0.0.2",
    "depends" : ['base', 'sale', 'purchase', 'account', 'sale_stock', 'mail', 'product', 'stock', 'fleet','sale_management'],
    "author": "BrowseInfo",
    "summary": "Fleet repair vehicle repair car Maintenance auto-fleet service repair Car Maintenance Repair workshop automobile repair Automotive Service repair Automotive repair machine repair workshop equipment repair service Repair auto repair shop Auto Shop repair",
    "description": """
    BrowseInfo developed a new odoo/OpenERP module apps.
    This module use for autorepair industry , workshop management, Car Repair service industry, Spare parts industry. Fleet repair management. Vehicle Repair shop, Mechanic workshop, Mechanic repair software.Maintenance and Repair car. Car Maintenance Spare Part Supply. Car Servicing, Auto Servicing, Auto mobile Service, Bike Repair Service. Maintenance and Operation.Car Maintenance Repair management module helps to manage repair order, repair diagnosis, Diagnosis report, Diagnosis analysis, Quote for Repair, Invoice for Repair, Repair invoice, Repair orders, Workorder for repair, Fleet Maintenance.
    product repair, car workshop management, auto workshop management, repair workshop, workorder for product, 
This module use for following industry.
    -Laptop Repair, Computer servicing, Maintenance and Operation, Maintenance Repair, Service Industry. Computer Repair.Product Repair. car Maintenance, Repair and Maintenance. Product Repair management
      repair order
      repair workflow
      product repair management
      car repair management
      car repair order
      car repair Diagnosis
      car repair workorder
      car repair management with dynamic flow
      repair order for car
      car repair receipt
      Maintenance and repair management for car
      car Maintenance and repair 

      fleet repair order
      fleet repair workflow
      fleet repair management
      fleetrepair order
      fleet repair Diagnosis
      fleet repair workorder
      fleet repair management with dynamic flow
      repair order for fleet
      fleet repair receipt
      Maintenance and repair management for fleet
      fleet Maintenance and repair  
      car repair dynamic workflow
      fleet repair dynamic workflow
      vehicle repair
      workshop automobile
      automobile workshop
      automobile repair

Odoo Laptop Repair Computer servicing Maintenance and Operation Maintenance Repair
Odoo repair Service Industry Computer Repair Product Repair car Maintenance Repair and Maintenance Product Repair management
Odoo repair order repair workflow product repair management
Odoo car repair management car repair order car repair Diagnosis car repair workorder car repair management with dynamic flow
Odoo repair order for car
Odoo car repair receipt Maintenance and repair management for car
Odoo car Maintenance and repair 
Odoo fleet repair order fleet repair workflow fleet repair management fleet Diagnosis
Odoo fleetrepair order fleet repair Diagnosis fleet repair workorder
Odoo fleet repair management with dynamic flow repair order for fleet fleet repair receipt
Odoo Maintenance and repair management for fleet odoo fleet Maintenance and repair 

Odoo vehicle repair order vehicle repair workflow vehicle repair management vehicle Diagnosis
Odoo vehicle repair order vehicle repair Diagnosis vehicle repair workorder
Odoo vehicle repair management with dynamic flow repair order for vehicle repair receipt
Odoo Maintenance and repair management for vehicle odoo vehicle Maintenance and repair  
Odoo car repair dynamic workflow fleet repair dynamic workflow
Odoo vehicle repair workshop automobile automobile workshop automobile repair
Odoo bike repair bike workshop repair vehicle workshop
Odoo product repair management car repair management machine repair management
Odoo car repair order car repair Diagnosis car repair workorder car repair management with dynamic flow
Odoo repair order for car car repair receipt Maintenance and repair management for car 
Odoo car Maintenance and repair auto-fleet repair auto parts repair car parts repair fleet parts repair
Odoo fleet repair order fleet repair workflow fleet repair management
Odoo fleetrepair order fleet repair Diagnosis fleet repair workorder fleet repair management with dynamic flow
Odoo repair order for fleet odoo fleet repair receipt
Odoo Maintenance and repair management for fleet odoo fleet Maintenance and repair  
odoo car repair dynamic workflow fleet repair dynamic workflow vehicle repair
Odoo workshop automobile automobile workshop
odoo automobile repair vehicle workshop
Odoo car Maintenance and repair auto repair management 
Odoo repair auto 
Odoo Automotive repair shop management auto repair shop
Odoo Auto Shop Management
Odoo Garage Management
Odoo Vehicle Service Management System
Odoo car service center
Odoo service center Automotive and Repair Shop Management
Odoo service Shop Management repair Auto Workshop
Odoo car workshop Collision Repair Auto Body Shop Management
odoo Auto Body Shop Management Body Shop Management BodyShop Management
Odoo automotive repair Vehicle Management Services Automotive Management
Odoo Repairs Management Maintenance Repairs Management
Odoo auto repair shop management software auto repair software free
Odoo auto service auto spareparts auto repair industry automotive workshop management software       vehicle workshop

Odoo Machine Repair Machine Diagnosis Machine Work Order machine workorder repair
  Odoo Laptop Repair Computer servicing Maintenance and Operation Maintenance Repair Service Industry. 
  Odoo Computer Repair Product Repair Machine Maintenance Repair and Maintenance Product Repair management
  Odoo repair order repair workflow in odoo
  Odoo product repair management machine repair order machine repair Diagnosis machine repair workorder
  Odoo machine repair management with dynamic flow repair order for machine
  Odoo machine repair receipt Maintenance and repair management for machine Odoo machine Maintenance and repair  
  Odoo Product repair order Product repair workflow in odoo
  Odoo product repair management Product repair order Product repair Diagnosis Product repair workorder
  Odoo Product repair management with dynamic flow repair order for Product
  Odoo Product repair receipt Maintenance and repair management for Product Odoo Product Maintenance and repair 

Odoo machine repair workshop repair for machine product workshop repair for product
Odoo Repair Management service Repair Management service Management
Odoo Washing Machine Repair Service Machine Repair Service Repair Service
Odoo machine repairs workshop Service Odoo Service workshop

Odoo machine parts workshop machine repair workshop management

Odoo repair order report repair receipt report repair Diagnosis report repair workorder report
Odoo car repair order report car repair receipt report car repair Diagnosis report car repair workorder report
Odoo machine repair order report machine repair receipt report machine repair Diagnosis report machine repair workorder report
   car Maintenance and repair 
auto repair management 
repair auto 
Automotive repair shop management
auto repair shop
Auto Shop Management
Garage Management
Vehicle Service Management System
car service center
service center
Automotive and Repair Shop Management
Shop Management
Auto Workshop
car workshop
Collision Repair & Auto Body Shop Management
Auto Body Shop Management
Body Shop Management
BodyShop Management
automotive repair
Vehicle Management Services
Automotive Management
Repairs Management 
Maintenance & Repairs Management
auto repair shop management software

auto repair software free
auto service
auto spareparts 
auto repair industry


automotive workshop management software


    """,
    'category': 'Industries',
    'price': 129,
    'currency': "EUR",
    "website" : "https://www.browseinfo.in",
    "data" :[
        'security/fleet_repair_security.xml',
        'security/ir.model.access.csv',
        'wizard/fleet_repair_assign_to_head_tech_view.xml',
        'wizard/fleet_diagnose_assign_to_technician_view.xml',
        'views/fleet_repair_view.xml',
        'views/fleet_repair_sequence.xml',
        'views/fleet_diagnose_view.xml',
        # 'views/fleet_diagnose_workflow.xml',
        # 'views/fleet_repair_workflow.xml',
        'views/fleet_workorder_sequence.xml',
        'views/fleet_workorder_view.xml',
        # 'views/fleet_workorder_workflow.xml',
        'views/custom_sale_view.xml',
        'report/fleet_repair_label_view.xml',
        'report/fleet_repair_label_menu.xml',
        'report/fleet_repair_receipt_view.xml',
        'report/fleet_repair_receipt_menu.xml',
        'report/fleet_diagnostic_request_report_view.xml',
        'report/fleet_diagnostic_request_report_menu.xml',
        'report/fleet_diagnostic_result_report_view.xml',
        'report/fleet_diagnostic_result_report_menu.xml',
        'report/fleet_workorder_report_view.xml',
        'report/fleet_workorder_report_menu.xml',
    ],
    'qweb':[
    ],
    "auto_install": False,
    "installable": True,
    'live_test_url':'https://www.youtube.com/watch?v=V6OCodztNA4&t=133s',
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
