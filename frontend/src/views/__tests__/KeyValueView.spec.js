import { shallowMount } from '@vue/test-utils'
import flushPromises from 'flush-promises'
import KeyValueView from '../KeyValueView.vue'
import PutForm from '../../components/PutForm.vue'
import GetForm from '../../components/GetForm.vue'
import DeleteForm from '../../components/DeleteForm.vue'
import axios from 'axios'
import { nextTick } from 'vue'

vi.mock('axios')

describe('KeyValueView.vue', () => {
  let wrapper
  beforeEach(() => {
    wrapper = shallowMount(KeyValueView, {
      global: { stubs: ['Navbar', 'Footer'] }
    })
  })

  it('renders all three forms', () => {
    expect(wrapper.findComponent(PutForm).exists()).toBe(true)
    expect(wrapper.findComponent(GetForm).exists()).toBe(true)
    expect(wrapper.findComponent(DeleteForm).exists()).toBe(true)
  })

  it('shows success alert on PUT', async () => {
    axios.put.mockResolvedValue({ data: {} })
    wrapper.findComponent(PutForm).vm.$emit('submit', { key: 'k', value: 'v' })
    await flushPromises()
    await nextTick()
    const alert = wrapper.find('.alert-success')
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain('Sucesso! Guardada a key "k"')
  })

  it('shows error alert on GET failure', async () => {
    axios.get.mockRejectedValue({ response: { data: { detail: 'not found' } } })
    wrapper.findComponent(GetForm).vm.$emit('submit', 'nokey')
    await flushPromises()
    await nextTick()
    expect(wrapper.find('.alert-danger').text()).toContain('Erro: not found')
  })

  it('shows success alert on DELETE', async () => {
    axios.delete.mockResolvedValue({ data: {} })
    wrapper.findComponent(DeleteForm).vm.$emit('submit', 'delkey')
    await flushPromises()
    await nextTick()
    expect(wrapper.find('.alert-success').text()).toContain('Sucesso! Removida a key "delkey"')
  })
})