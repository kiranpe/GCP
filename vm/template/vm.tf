resource "google_compute_instance_from_template" "vm" {
   name = var.vm_name
   zone = var.zone

   source_instance_template = google_compute_instance_template.vm_tpl.id

   labels = local.vm_labels
}
