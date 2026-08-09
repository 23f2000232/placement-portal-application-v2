<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import driveService from '@/services/company-placement-drive.service'
import companyService from '@/services/company.service'
import { getCurrentUser } from '@/utils/auth'

const loading = ref(true)
const error = ref('')
const selectedApplications = ref([])
const selectedApplicationId = ref('')
const application = ref(null)
const generating = ref(false)
const generatedAt = ref('')
const company = getCurrentUser()

const today = new Date()
const toInputDate = (date) => date.toISOString().slice(0, 10)
const addDays = (date, days) => new Date(date.getTime() + days * 24 * 60 * 60 * 1000)
const letter = ref({
  companyName: company?.company_name || 'Your Company',
  issuerName: company?.contact_person || '',
  annualCompensation: '',
  joiningDate: toInputDate(addDays(today, 30)),
  acceptanceDeadline: toInputDate(addDays(today, 7)),
  terms: 'This offer is subject to successful document verification and the company policies in effect on the joining date.',
})

const selectedApplication = computed(() =>
  selectedApplications.value.find((item) => item.id === selectedApplicationId.value),
)

const dateLabel = (date) =>
  new Date(`${date}T00:00:00`).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })

const escapeHtml = (value) =>
  String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')

const loadSelectedApplications = async () => {
  loading.value = true
  error.value = ''
  try {
    const drives = (await driveService.getCompanyPlacementDrives({ page: 1, size: 100 })).items
    const pages = await Promise.all(
      drives.map((drive) => companyService.getDriveApplications(drive.id, { page: 1, size: 100 })),
    )
    selectedApplications.value = pages.flatMap((page) => page.items).filter((item) => item.application_status === 'SELECTED')
    if (selectedApplications.value.length) {
      selectedApplicationId.value = selectedApplications.value[0].id
      await loadApplication()
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load selected applications.'
  } finally {
    loading.value = false
  }
}

const loadApplication = async () => {
  if (!selectedApplicationId.value) return
  generating.value = true
  error.value = ''
  try {
    application.value = await companyService.getApplication(selectedApplicationId.value)
    letter.value.annualCompensation = application.value.salary_package
      ? `₹${Number(application.value.salary_package).toLocaleString('en-IN')} per annum`
      : ''
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load this application.'
  } finally {
    generating.value = false
  }
}

const downloadOfferLetter = () => {
  if (!application.value) return

  const generatedDate = new Date().toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
  const candidate = application.value
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Demo Offer Letter</title>
<style>body{font-family:Arial,sans-serif;color:#1f2937;line-height:1.6;margin:0}main{max-width:760px;margin:40px auto;padding:48px;border:1px solid #d1d5db}.notice{background:#fff3cd;border:1px solid #ffecb5;color:#664d03;padding:12px;font-weight:700}.header{border-bottom:3px solid #0d6efd;margin:28px 0;padding-bottom:16px}h1{color:#0d6efd;font-size:28px;margin:0}.muted{color:#6b7280}.signature{margin-top:48px}@media print{main{border:0;margin:0;max-width:none}.notice{display:none}}</style>
</head><body><main><div class="notice">DEMO OFFER LETTER — NOT LEGALLY BINDING</div><div class="header"><h1>${escapeHtml(letter.value.companyName)}</h1><div class="muted">Date: ${generatedDate}</div></div>
<p>Dear ${escapeHtml(candidate.student_name)},</p><p>We are pleased to offer you the position of <strong>${escapeHtml(candidate.job_title)}</strong> at ${escapeHtml(letter.value.companyName)}${candidate.job_location ? `, ${escapeHtml(candidate.job_location)}` : ''}.</p>
<p>Your annual compensation will be <strong>${escapeHtml(letter.value.annualCompensation || 'as mutually agreed')}</strong>. Your proposed joining date is <strong>${dateLabel(letter.value.joiningDate)}</strong>.</p>
<p>${escapeHtml(letter.value.terms)}</p><p>Please confirm your acceptance by <strong>${dateLabel(letter.value.acceptanceDeadline)}</strong>.</p>
<p>We look forward to having you on our team.</p><div class="signature"><strong>${escapeHtml(letter.value.issuerName || 'Authorized Signatory')}</strong><br>${escapeHtml(letter.value.companyName)}</div></main></body></html>`

  const blob = new Blob([html], { type: 'text/html;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = `demo-offer-letter-${candidate.student_name.replaceAll(/[^a-z0-9]/gi, '-').toLowerCase()}.html`
  anchor.click()
  URL.revokeObjectURL(url)
  generatedAt.value = new Date().toLocaleString('en-IN')
}

onMounted(loadSelectedApplications)
</script>

<template>
  <AppLayout>
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-start mb-4">
        <div><h2 class="mb-1">Demo Offer Letter Generator</h2><p class="text-muted mb-0">Generate a downloadable sample offer letter for a selected candidate.</p></div>
        <span class="badge text-bg-warning">Demo only</span>
      </div>
      <ErrorAlert v-if="error" :message="error" />
      <LoadingSpinner v-else-if="loading" />
      <EmptyState v-else-if="!selectedApplications.length" title="No selected candidates" message="Mark an application as selected before generating an offer letter." />
      <form v-else class="card shadow-sm" @submit.prevent="downloadOfferLetter">
        <div class="card-body"><div class="alert alert-warning"><strong>Not legally binding.</strong> This tool creates a demo HTML document for project demonstration only.</div>
          <div class="row g-3"><div class="col-md-6"><label class="form-label">Selected candidate</label><select v-model="selectedApplicationId" class="form-select" @change="loadApplication"><option v-for="item in selectedApplications" :key="item.id" :value="item.id">{{ item.student_name }} — {{ item.roll_number }}</option></select></div><div class="col-md-6"><label class="form-label">Position</label><input :value="application?.job_title || ''" class="form-control" readonly></div>
            <div class="col-md-6"><label class="form-label">Company name</label><input v-model.trim="letter.companyName" required class="form-control"></div><div class="col-md-6"><label class="form-label">Authorized signatory</label><input v-model.trim="letter.issuerName" class="form-control" placeholder="e.g. HR Manager"></div>
            <div class="col-md-4"><label class="form-label">Annual compensation</label><input v-model.trim="letter.annualCompensation" required class="form-control" placeholder="e.g. ₹8,00,000 per annum"></div><div class="col-md-4"><label class="form-label">Joining date</label><input v-model="letter.joiningDate" required type="date" class="form-control"></div><div class="col-md-4"><label class="form-label">Acceptance deadline</label><input v-model="letter.acceptanceDeadline" required type="date" class="form-control"></div>
            <div class="col-12"><label class="form-label">Terms</label><textarea v-model.trim="letter.terms" required rows="3" class="form-control" /></div></div>
        </div><div class="card-footer bg-white d-flex justify-content-between align-items-center"><small v-if="generatedAt" class="text-success">Last generated: {{ generatedAt }}</small><span v-else></span><button class="btn btn-primary" :disabled="generating || !application">Download demo offer letter</button></div>
      </form>
    </div>
  </AppLayout>
</template>
